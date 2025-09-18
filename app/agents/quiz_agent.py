from sqlalchemy.orm import Session
from app.models.mcq import MCQ
import random

class QuizAgent:
    def create_quiz(self, db: Session, syllabus_id: int, num_questions: int = 10) -> list:
        mcqs = db.query(MCQ).filter(MCQ.syllabus_id == syllabus_id).all()
        if not mcqs:
            return []
        
        if len(mcqs) < num_questions:
            num_questions = len(mcqs)
        
        selected_mcqs = random.sample(mcqs, num_questions)
        return selected_mcqs
    
    def calculate_score(self, answers: dict, correct_answers: dict) -> float:
        correct = sum(1 for q_id, answer in answers.items() 
                     if correct_answers.get(q_id) == answer)
        return (correct / len(answers)) * 100 if answers else 0