from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY
import json
import re

class GeneralAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it",
            temperature=0.5
        )
        self.agent_type = "general"
    
    def health_check(self) -> dict:
        """Check agent health and capabilities"""
        try:
            response = self.llm.invoke([HumanMessage(content="What is the capital of France?")])
            return {
                "status": "healthy",
                "agent_type": self.agent_type,
                "capabilities": ["general_mcqs", "conceptual_questions", "theory"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "agent_type": self.agent_type,
                "error": str(e)
            }
    
    def generate_general_mcqs(self, topic: str, content: str, count: int = 3) -> list:
        """Generate general knowledge MCQs for non-math subjects"""
        prompt = f"""
        Create {count} conceptual multiple choice questions for: {topic}
        
        Content: {content[:1000]}
        
        Focus on:
        - Theoretical concepts
        - Definitions and explanations
        - Understanding and application
        - Factual knowledge
        
        Return ONLY valid JSON:
        [{{
            "question": "What is the definition of...",
            "option_a": "Concept explanation 1",
            "option_b": "Concept explanation 2",
            "option_c": "Concept explanation 3",
            "option_d": "Concept explanation 4",
            "correct_answer": "A",
            "explanation": "Detailed explanation",
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
            
            # Fallback general MCQ
            return [{
                "question": f"What is the main concept of {topic}?",
                "option_a": "Concept A",
                "option_b": "Concept B",
                "option_c": "Concept C", 
                "option_d": "Concept D",
                "correct_answer": "A",
                "explanation": f"This explains the core idea of {topic}",
                "difficulty": "easy"
            }]
            
        except Exception as e:
            print(f"General agent error: {e}")
            return []
    
    def explain_concept(self, concept: str) -> dict:
        """Explain general concepts in detail"""
        prompt = f"""
        Explain this concept in detail:
        {concept}
        
        Provide:
        1. Definition
        2. Key points
        3. Examples
        4. Applications
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return {
                "explanation": response.content,
                "agent": self.agent_type
            }
        except Exception as e:
            return {"error": str(e), "agent": self.agent_type}