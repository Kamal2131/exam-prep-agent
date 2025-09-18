from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class MCQ(Base):
    __tablename__ = "mcqs"
    
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    question = Column(Text)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(String)
    explanation = Column(Text)
    topic = Column(String)
    
    syllabus = relationship("Syllabus")