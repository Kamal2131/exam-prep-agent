from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from .db import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    questions = Column(Text)  # JSON string of question IDs
    score = Column(Float, default=0.0)
    total_questions = Column(Integer)
    
    syllabus = relationship("Syllabus")