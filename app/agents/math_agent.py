from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY
import json
import re

class MathAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it",
            temperature=0.3
        )
        self.agent_type = "math"
    
    def health_check(self) -> dict:
        """Check agent health and capabilities"""
        try:
            response = self.llm.invoke([HumanMessage(content="What is 2+2?")])
            return {
                "status": "healthy",
                "agent_type": self.agent_type,
                "capabilities": ["math_mcqs", "math_problems", "calculations"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "agent_type": self.agent_type,
                "error": str(e)
            }
    
    def generate_math_mcqs(self, topic: str, content: str, count: int = 3) -> list:
        """Generate math-specific MCQs with calculations and formulas"""
        prompt = f"""
        Create {count} mathematical multiple choice questions for: {topic}
        
        Content: {content[:1000]}
        
        Focus on:
        - Calculations and formulas
        - Problem-solving steps
        - Mathematical concepts
        - Numerical answers
        
        Return ONLY valid JSON:
        [{{
            "question": "Calculate the value of...",
            "option_a": "Numerical answer 1",
            "option_b": "Numerical answer 2",
            "option_c": "Numerical answer 3",
            "option_d": "Numerical answer 4",
            "correct_answer": "A",
            "explanation": "Step-by-step solution",
            "difficulty": "medium"
        }}]
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                mcqs = json.loads(json_match.group())
                return mcqs if isinstance(mcqs, list) else []
            
            # Fallback math MCQ
            return [{
                "question": f"What is the fundamental concept in {topic}?",
                "option_a": "Formula A",
                "option_b": "Formula B", 
                "option_c": "Formula C",
                "option_d": "Formula D",
                "correct_answer": "A",
                "explanation": f"This is the basic principle of {topic}",
                "difficulty": "easy"
            }]
            
        except Exception as e:
            print(f"Math agent error: {e}")
            return []
    
    def solve_problem(self, problem: str) -> dict:
        """Solve mathematical problems step by step"""
        prompt = f"""
        Solve this mathematical problem step by step:
        {problem}
        
        Provide:
        1. Solution steps
        2. Final answer
        3. Verification
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return {
                "solution": response.content,
                "agent": self.agent_type
            }
        except Exception as e:
            return {"error": str(e), "agent": self.agent_type}