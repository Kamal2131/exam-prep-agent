from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
from .supervisor_agent import SupervisorAgent
from .syllabus_agent import SyllabusAgent
import os
import random
import logging

logger = logging.getLogger(__name__)

# Set LangSmith environment variables if not already set
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "exam-prep-agent")

class ExamWorkflowState(TypedDict):
    syllabus_content: str
    syllabus_id: int
    topics: List[str]
    mcqs: List[Dict[str, Any]]
    flashcards: List[Dict[str, Any]]
    quiz_questions: List[Any]
    user_answers: Dict[str, str]
    exam_results: Dict[str, Any]
    current_step: str
    agent_health: Dict[str, Any]
    errors: List[str]

class ExamWorkflow:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.syllabus_agent = SyllabusAgent()
    
    def extract_topics_node(self, state: ExamWorkflowState) -> Dict[str, Any]:
        """Extract topics from syllabus content"""
        try:
            logger.info("Extracting topics from syllabus")
            topics = self.syllabus_agent.extract_topics(state["syllabus_content"])
            logger.info(f"Extracted {len(topics)} topics: {topics}")
            
            return {
                "topics": topics,
                "current_step": "topics_extracted",
                "errors": state.get("errors", [])
            }
        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"Topic extraction failed: {str(e)}")
            return {
                "topics": ["General Topics"],
                "current_step": "topics_extracted",
                "errors": errors
            }
    
    def check_agent_health_node(self, state: ExamWorkflowState) -> Dict[str, Any]:
        """Check health of all agents before proceeding"""
        try:
            logger.info("Checking agent health")
            health_status = self.supervisor.check_agents_health()
            logger.info(f"Agent health check complete: {health_status['healthy_agents']}/{health_status['total_agents']} healthy")
            
            return {
                "agent_health": health_status,
                "current_step": "health_checked",
                "errors": state.get("errors", [])
            }
        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"Health check failed: {str(e)}")
            return {
                "agent_health": {"status": "unknown"},
                "current_step": "health_checked", 
                "errors": errors
            }
    
    def generate_mcqs_node(self, state: ExamWorkflowState) -> Dict[str, Any]:
        """Generate MCQs using supervisor delegation"""
        try:
            logger.info("Generating MCQs with supervisor delegation")
            all_mcqs = []
            
            for topic in state["topics"]:
                result = self.supervisor.delegate_mcq_generation(
                    topic, 
                    state["syllabus_content"], 
                    count=3
                )
                
                if result["status"] == "success":
                    # Add topic and agent info to each MCQ
                    for mcq in result["mcqs"]:
                        mcq["topic"] = topic
                        mcq["generated_by"] = result["agent_used"]
                    all_mcqs.extend(result["mcqs"])
                else:
                    logger.warning(f"Failed to generate MCQs for topic: {topic}")
            
            return {
                "mcqs": all_mcqs,
                "current_step": "mcqs_generated",
                "errors": state.get("errors", [])
            }
        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"MCQ generation failed: {str(e)}")
            return {
                "mcqs": [],
                "current_step": "mcqs_generated",
                "errors": errors
            }
    
    def create_quiz_node(self, state: ExamWorkflowState) -> Dict[str, Any]:
        """Create quiz from generated MCQs"""
        try:
            mcqs = state.get("mcqs", [])
            
            # Select exactly 10 questions for quiz
            if len(mcqs) > 10:
                quiz_questions = random.sample(mcqs, 10)
            else:
                quiz_questions = mcqs
            
            return {
                "quiz_questions": quiz_questions,
                "current_step": "quiz_created",
                "errors": state.get("errors", [])
            }
        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"Quiz creation failed: {str(e)}")
            return {
                "quiz_questions": [],
                "current_step": "quiz_created",
                "errors": errors
            }
    
    def evaluate_exam_node(self, state: ExamWorkflowState) -> Dict[str, Any]:
        """Evaluate exam answers using supervisor"""
        try:
            # Mock question objects for evaluation
            class MockQuestion:
                def __init__(self, mcq_data, idx):
                    self.id = idx
                    self.question = mcq_data["question"]
                    self.correct_answer = mcq_data["correct_answer"]
                    self.explanation = mcq_data.get("explanation", "")
                    self.topic = mcq_data.get("topic", "General")
            
            questions = [MockQuestion(mcq, idx) for idx, mcq in enumerate(state["quiz_questions"])]
            user_answers = state.get("user_answers", {})
            
            results = self.supervisor.evaluate_exam_answers(questions, user_answers)
            
            return {
                "exam_results": results,
                "current_step": "exam_evaluated",
                "errors": state.get("errors", [])
            }
        except Exception as e:
            errors = state.get("errors", [])
            errors.append(f"Exam evaluation failed: {str(e)}")
            return {
                "exam_results": {"error": str(e)},
                "current_step": "exam_evaluated",
                "errors": errors
            }
    
    def build_workflow(self) -> StateGraph:
        """Build the complete exam preparation workflow"""
        workflow = StateGraph(ExamWorkflowState)
        
        # Add nodes
        workflow.add_node("extract_topics", self.extract_topics_node)
        workflow.add_node("check_health", self.check_agent_health_node)
        workflow.add_node("generate_mcqs", self.generate_mcqs_node)
        workflow.add_node("create_quiz", self.create_quiz_node)
        workflow.add_node("evaluate_exam", self.evaluate_exam_node)
        
        # Define workflow edges
        workflow.set_entry_point("extract_topics")
        workflow.add_edge("extract_topics", "check_health")
        workflow.add_edge("check_health", "generate_mcqs")
        workflow.add_edge("generate_mcqs", "create_quiz")
        workflow.add_edge("create_quiz", END)
        
        # Conditional edge for evaluation (only when user answers are provided)
        def should_evaluate(state: ExamWorkflowState) -> str:
            if state.get("user_answers"):
                return "evaluate_exam"
            return END
        
        workflow.add_conditional_edges(
            "create_quiz",
            should_evaluate,
            {
                "evaluate_exam": "evaluate_exam",
                END: END
            }
        )
        workflow.add_edge("evaluate_exam", END)
        
        return workflow.compile()
    
    def run_exam_preparation(self, syllabus_content: str, syllabus_id: int) -> Dict[str, Any]:
        """Run the complete exam preparation workflow"""
        workflow = self.build_workflow()
        
        initial_state = {
            "syllabus_content": syllabus_content,
            "syllabus_id": syllabus_id,
            "current_step": "start",
            "errors": []
        }
        
        try:
            result = workflow.invoke(initial_state)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "current_step": "failed",
                "errors": [str(e)]
            }
    
    def run_exam_evaluation(self, quiz_questions: List[Dict], user_answers: Dict[str, str]) -> Dict[str, Any]:
        """Run exam evaluation directly using supervisor"""
        try:
            if not quiz_questions:
                return {
                    "total_questions": 0,
                    "correct_answers": 0,
                    "score_percentage": 0,
                    "grade": "F",
                    "detailed_results": [],
                    "feedback": "No questions available for evaluation",
                    "error": "No quiz questions provided"
                }
            
            # Create mock question objects for evaluation
            class MockQuestion:
                def __init__(self, mcq_data):
                    self.id = mcq_data["id"]
                    self.question = mcq_data["question"]
                    self.correct_answer = mcq_data["correct_answer"]
                    self.explanation = mcq_data.get("explanation", "")
                    self.topic = mcq_data.get("topic", "General")
            
            questions = [MockQuestion(mcq) for mcq in quiz_questions]
            
            # Use supervisor to evaluate
            results = self.supervisor.evaluate_exam_answers(questions, user_answers)
            return results
            
        except Exception as e:
            return {
                "total_questions": 0,
                "correct_answers": 0,
                "score_percentage": 0,
                "grade": "F",
                "detailed_results": [],
                "feedback": f"Evaluation failed: {str(e)}",
                "error": str(e)
            }