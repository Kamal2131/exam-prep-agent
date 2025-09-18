from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.models.db import get_db
from app.models.syllabus import Syllabus
from app.models.mcq import MCQ
from app.models.quiz import Quiz
from app.agents.exam_workflow import ExamWorkflow
from app.utils.pdf_loader import extract_text_from_pdf
from pydantic import BaseModel
from typing import Dict
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ExamAnswers(BaseModel):
    answers: Dict[str, str]

@router.post("/syllabus/upload")
async def upload_syllabus(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process syllabus file"""
    try:
        logger.info(f"Uploading syllabus file: {file.filename}")
        
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.txt')):
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            text_content = extract_text_from_pdf(content)
        else:
            text_content = content.decode('utf-8')
        
        logger.info(f"Extracted {len(text_content)} characters from file")
        
        # Extract topics using syllabus agent
        from app.agents.syllabus_agent import SyllabusAgent
        syllabus_agent = SyllabusAgent()
        topics = syllabus_agent.extract_topics(text_content)
        
        # Get current user from token
        auth_header = request.headers.get("Authorization")
        logger.info(f"Auth header: {auth_header}")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")
        
        token = auth_header.split(" ")[1]
        logger.info(f"Token: {token[:20]}...")
        
        from app.auth.jwt_handler import verify_token
        user_data = verify_token(token)
        logger.info(f"User data: {user_data}")
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Save to database
        syllabus = Syllabus(
            title=file.filename,
            content=text_content,
            topics=json.dumps(topics),
            user_id=user_data["user_id"]
        )
        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)
        
        logger.info(f"Syllabus saved with ID: {syllabus.id}")
        
        return {
            "id": syllabus.id,
            "title": syllabus.title,
            "topics": topics,
            "content_length": len(text_content)
        }
        
    except Exception as e:
        logger.error(f"Error uploading syllabus: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/prepare-exam/{syllabus_id}")
async def prepare_exam_workflow(syllabus_id: int, db: Session = Depends(get_db)):
    """Run complete exam preparation workflow using LangGraph"""
    try:
        logger.info(f"Starting exam preparation for syllabus_id: {syllabus_id}")
        
        # Get syllabus
        syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
        if not syllabus:
            logger.error(f"Syllabus not found: {syllabus_id}")
            raise HTTPException(status_code=404, detail="Syllabus not found")
        
        logger.info(f"Found syllabus: {syllabus.title}")
        
        # Initialize workflow
        workflow = ExamWorkflow()
        
        # Run exam preparation
        logger.info("Running exam preparation workflow")
        result = workflow.run_exam_preparation(syllabus.content, syllabus_id)
        
        # Save MCQs to database
        mcqs_saved = 0
        if result.get("mcqs"):
            logger.info(f"Saving {len(result['mcqs'])} MCQs to database")
            try:
                for mcq_data in result["mcqs"]:
                    if all(key in mcq_data for key in ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer"]):
                        mcq = MCQ(
                            syllabus_id=syllabus_id,
                            question=mcq_data["question"],
                            option_a=mcq_data["option_a"],
                            option_b=mcq_data["option_b"],
                            option_c=mcq_data["option_c"],
                            option_d=mcq_data["option_d"],
                            correct_answer=mcq_data["correct_answer"],
                            explanation=mcq_data.get("explanation", ""),
                            topic=mcq_data.get("topic", "General")
                        )
                        db.add(mcq)
                        mcqs_saved += 1
                    else:
                        logger.warning(f"Skipping invalid MCQ data: {mcq_data}")
                db.commit()
                logger.info(f"Successfully saved {mcqs_saved} MCQs")
            except Exception as e:
                db.rollback()
                logger.error(f"Failed to save MCQs: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to save MCQs: {str(e)}")
        else:
            logger.warning("No MCQs generated from workflow")
        
        return {
            "status": "success",
            "syllabus_id": syllabus_id,
            "topics": result.get("topics", []),
            "mcqs_generated": mcqs_saved,
            "quiz_questions": len(result.get("quiz_questions", [])),
            "agent_health": result.get("agent_health", {}),
            "errors": result.get("errors", []),
            "workflow_complete": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/quiz/{syllabus_id}")
async def get_quiz_questions(syllabus_id: int, db: Session = Depends(get_db)):
    """Get quiz questions for exam"""
    try:
        # Check if syllabus exists
        syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")
        
        mcqs = db.query(MCQ).filter(MCQ.syllabus_id == syllabus_id).limit(10).all()
        
        if not mcqs:
            raise HTTPException(status_code=404, detail="No MCQs found. Please generate MCQs first.")
        
        quiz_questions = []
        for mcq in mcqs:
            quiz_questions.append({
                "id": mcq.id,
                "question": mcq.question,
                "option_a": mcq.option_a,
                "option_b": mcq.option_b,
                "option_c": mcq.option_c,
                "option_d": mcq.option_d,
                "topic": mcq.topic
            })
        
        return {
            "quiz_questions": quiz_questions,
            "total_questions": len(quiz_questions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/submit-exam/{syllabus_id}")
async def submit_exam_workflow(syllabus_id: int, exam_answers: ExamAnswers, db: Session = Depends(get_db)):
    """Submit exam and get detailed evaluation using supervisor agent"""
    try:
        logger.info(f"Starting exam evaluation for syllabus_id: {syllabus_id}")
        
        # Get quiz questions (limit to 10)
        mcqs = db.query(MCQ).filter(MCQ.syllabus_id == syllabus_id).limit(10).all()
        
        if not mcqs:
            logger.error(f"No MCQs found for syllabus_id: {syllabus_id}")
            raise HTTPException(status_code=404, detail="No MCQs found for this syllabus. Please generate MCQs first.")
        
        logger.info(f"Found {len(mcqs)} MCQs for evaluation")
        
        # Convert to quiz format
        quiz_questions = []
        for mcq in mcqs:
            quiz_questions.append({
                "id": mcq.id,
                "question": mcq.question,
                "option_a": mcq.option_a,
                "option_b": mcq.option_b,
                "option_c": mcq.option_c,
                "option_d": mcq.option_d,
                "correct_answer": mcq.correct_answer,
                "explanation": mcq.explanation,
                "topic": mcq.topic
            })
        
        logger.info(f"User submitted {len(exam_answers.answers)} answers")
        
        # Initialize workflow for evaluation
        workflow = ExamWorkflow()
        
        # Run evaluation
        results = workflow.run_exam_evaluation(quiz_questions, exam_answers.answers)
        logger.info(f"Evaluation complete - Score: {results.get('score_percentage', 0)}%")
        
        # Save quiz results to database
        quiz = Quiz(
            syllabus_id=syllabus_id,
            questions=json.dumps([q["id"] for q in quiz_questions]),
            score=results.get("score_percentage", 0),
            total_questions=len(quiz_questions)
        )
        db.add(quiz)
        db.commit()
        
        return {
            "status": "success",
            "quiz_id": quiz.id,
            "results": results,
            "supervisor_evaluated": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/agent-health")
async def check_agent_health():
    """Check health status of all agents"""
    try:
        workflow = ExamWorkflow()
        health_status = workflow.supervisor.check_agents_health()
        
        return {
            "status": "success",
            "health_check": health_status,
            "timestamp": "now"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))