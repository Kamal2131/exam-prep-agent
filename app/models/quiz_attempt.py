from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    score = Column(Float)
    total_questions = Column(Integer)
    answers = Column(Text)  # JSON string of user answers
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    syllabus = relationship("Syllabus")