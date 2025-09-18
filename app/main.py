from fastapi import FastAPI, Depends, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import html
from sqlalchemy.orm import Session
from app.models.db import get_db, engine, Base
from app.routes import workflow_routes, auth_routes
from app.utils.logger import logger

# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

app = FastAPI(title="Exam Prep Agent")
logger.info("FastAPI app initialized")
templates = Jinja2Templates(directory="app/templates")
templates.env.autoescape = True

@app.get("/test")
async def test():
    return {"message": "Server is working!"}

# Include routes
app.include_router(workflow_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("exam.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)