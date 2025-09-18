import os
from pydantic_settings import BaseSettings

class ProductionSettings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/examdb")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALLOWED_HOSTS: list = ["*"]  # Configure properly in production
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [".pdf", ".txt", ".docx"]
    
    # MCQ Generation
    MAX_MCQS_PER_TOPIC: int = 5
    MAX_TOPICS_PER_SYLLABUS: int = 20
    
    # Monitoring
    ENABLE_METRICS: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = ProductionSettings()