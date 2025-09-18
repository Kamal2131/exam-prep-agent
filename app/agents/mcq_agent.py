from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class MCQAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it"
        )
    
    def generate_mcqs(self, topic: str, syllabus_content: str, count: int = 3) -> list:
        prompt = f"""
        Create {count} multiple choice questions about: {topic}
        
        Content: {syllabus_content[:1000]}...
        
        Return ONLY valid JSON array:
        [{{
            "question": "What is..?",
            "option_a": "First option",
            "option_b": "Second option", 
            "option_c": "Third option",
            "option_d": "Fourth option",
            "correct_answer": "A",
            "explanation": "Brief explanation"
        }}]
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        logger.info(f"MCQ Response for {topic}: {content[:200]}...")
        
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                mcqs = json.loads(json_match.group())
                return mcqs if isinstance(mcqs, list) else []
            else:
                # Fallback: create simple MCQ
                return [{
                    "question": f"What is a key concept in {topic}?",
                    "option_a": "Option A",
                    "option_b": "Option B",
                    "option_c": "Option C", 
                    "option_d": "Option D",
                    "correct_answer": "A",
                    "explanation": f"This relates to {topic}"
                }]
        except Exception as e:
            logger.error(f"Error parsing MCQ response: {e}")
            return [{
                "question": f"What is important about {topic}?",
                "option_a": "Key concept 1",
                "option_b": "Key concept 2",
                "option_c": "Key concept 3",
                "option_d": "Key concept 4",
                "correct_answer": "A",
                "explanation": f"This is fundamental to {topic}"
            }]