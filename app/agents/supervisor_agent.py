from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY
from .math_agent import MathAgent
from .general_agent import GeneralAgent
import re
import logging

logger = logging.getLogger(__name__)

class SupervisorAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it",
            temperature=0.1
        )
        self.math_agent = MathAgent()
        self.general_agent = GeneralAgent()
        self.agents = {
            "math": self.math_agent,
            "general": self.general_agent
        }
    
    def classify_topic(self, topic: str, content: str) -> str:
        """Classify if topic is math-related or general"""
        prompt = f"""
        Classify this topic as either "math" or "general":
        
        Topic: {topic}
        Content: {content[:500]}
        
        Math topics include: algebra, geometry, calculus, statistics, trigonometry, arithmetic, equations, formulas, numbers
        General topics include: science, history, literature, biology, chemistry, physics concepts, social studies
        
        Return only: "math" or "general"
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            classification = response.content.strip().lower()
            
            # Check for math keywords
            math_keywords = ['math', 'algebra', 'geometry', 'calculus', 'trigonometry', 'equation', 'formula', 'number']
            if any(keyword in topic.lower() or keyword in classification for keyword in math_keywords):
                return "math"
            else:
                return "general"
                
        except Exception as e:
            pass
            # Default classification based on topic keywords
            math_keywords = ['math', 'algebra', 'geometry', 'calculus', 'trigonometry', 'statistics']
            return "math" if any(keyword in topic.lower() for keyword in math_keywords) else "general"
    
    def check_agents_health(self) -> dict:
        """Check health of all agents"""
        health_status = {}
        for agent_name, agent in self.agents.items():
            health_status[agent_name] = agent.health_check()
        
        return {
            "supervisor_status": "active",
            "agents_health": health_status,
            "total_agents": len(self.agents),
            "healthy_agents": sum(1 for status in health_status.values() if status["status"] == "healthy")
        }
    
    def delegate_mcq_generation(self, topic: str, content: str, count: int = 3) -> dict:
        """Delegate MCQ generation to appropriate agent"""
        try:
            # Classify the topic
            agent_type = self.classify_topic(topic, content)
            logger.info(f"Delegating '{topic}' to {agent_type} agent")
            
            # Check agent health before delegation
            agent = self.agents.get(agent_type, self.general_agent)
            health = agent.health_check()
            
            if health["status"] != "healthy":
                logger.warning(f"Agent {agent_type} is unhealthy, falling back to general agent")
                agent = self.general_agent
                agent_type = "general"
            
            # Generate MCQs using appropriate agent
            if agent_type == "math":
                mcqs = agent.generate_math_mcqs(topic, content, count)
            else:
                mcqs = agent.generate_general_mcqs(topic, content, count)
            
            logger.info(f"Generated {len(mcqs)} MCQs for topic '{topic}' using {agent_type} agent")
            
            return {
                "mcqs": mcqs,
                "agent_used": agent_type,
                "topic": topic,
                "count": len(mcqs),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "mcqs": [],
                "agent_used": "none",
                "topic": topic,
                "error": str(e),
                "status": "failed"
            }
    
    def evaluate_exam_answers(self, questions: list, answers: dict) -> dict:
        """Evaluate exam answers and calculate detailed scores"""
        try:
            total_questions = len(questions)
            correct_answers = 0
            detailed_results = []
            
            logger.info(f"Evaluating {total_questions} questions")
            
            for question in questions:
                q_id = str(question.id)
                user_answer = answers.get(q_id, "").upper()
                correct_answer = question.correct_answer.upper()
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    correct_answers += 1
                
                detailed_results.append({
                    "question_id": q_id,
                    "question": question.question,
                    "user_answer": answers.get(q_id, ""),
                    "correct_answer": question.correct_answer,
                    "is_correct": is_correct,
                    "explanation": question.explanation,
                    "topic": question.topic
                })
            
            score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            
            # Generate performance feedback
            feedback = self.generate_feedback(score_percentage, detailed_results)
            
            return {
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "score_percentage": round(score_percentage, 2),
                "grade": self.calculate_grade(score_percentage),
                "detailed_results": detailed_results,
                "feedback": feedback,
                "supervisor_evaluation": True
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade based on percentage"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"
    
    def generate_feedback(self, score: float, results: list) -> str:
        """Generate personalized feedback based on performance"""
        if score >= 90:
            return "Excellent work! You have mastered the concepts."
        elif score >= 70:
            return "Good job! Review the topics you missed for improvement."
        elif score >= 50:
            return "Fair performance. Focus on studying the weak areas."
        else:
            return "Needs improvement. Consider reviewing all topics thoroughly."