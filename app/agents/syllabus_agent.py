from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from app.config import GROQ_API_KEY

class SyllabusAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it"
        )
    
    def extract_topics(self, syllabus_content: str) -> list:
        prompt = f"""
        Extract 5-10 key topics from this syllabus content. Return ONLY a Python list format.
        
        Syllabus: {syllabus_content[:2000]}...
        
        Return format: ["Topic 1", "Topic 2", "Topic 3"]
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        topics_str = response.content.strip()
        
        # Try to extract list from response
        try:
            # Look for list pattern in response
            import re
            import ast
            list_match = re.search(r'\[.*?\]', topics_str, re.DOTALL)
            if list_match:
                topics = ast.literal_eval(list_match.group())
                return topics if isinstance(topics, list) else ["General Topics"]
            else:
                # Fallback: split by lines and clean
                lines = [line.strip().strip('"').strip("'") for line in topics_str.split('\n') if line.strip()]
                return lines[:10] if lines else ["General Topics"]
        except (ValueError, SyntaxError) as e:
            return ["General Topics", "Key Concepts", "Important Points"]