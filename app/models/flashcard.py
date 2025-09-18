from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    front = Column(Text)
    back = Column(Text)
    topic = Column(String)
    
    syllabus = relationship("Syllabus")