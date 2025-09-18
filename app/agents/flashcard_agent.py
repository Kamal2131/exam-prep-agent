from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY
import json

class FlashcardAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it"
        )
    
    def generate_flashcards(self, topic: str, syllabus_content: str, count: int = 10) -> list:
        prompt = f"""
        Generate {count} flashcards for the topic: {topic}
        Based on this syllabus content: {syllabus_content}
        
        Return JSON format:
        [{{
            "front": "Question or concept",
            "back": "Answer or explanation"
        }}]
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        try:
            flashcards = json.loads(response.content.strip())
            return flashcards if isinstance(flashcards, list) else []
        except:
            return []