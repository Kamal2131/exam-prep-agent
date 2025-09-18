from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base

class Syllabus(Base):
    __tablename__ = "syllabus"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    topics = Column(Text)  # JSON string of extracted topics
    created_at = Column(DateTime(timezone=True), server_default=func.now())