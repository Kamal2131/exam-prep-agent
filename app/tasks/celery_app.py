from celery import Celery
import os

celery_app = Celery(
    "exam_agent",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379"),
    include=["app.tasks.exam_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.tasks.exam_tasks.generate_mcqs_async": {"queue": "mcq_generation"},
        "app.tasks.exam_tasks.evaluate_exam_async": {"queue": "evaluation"},
    }
)