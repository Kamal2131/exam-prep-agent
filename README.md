# 🎓 AI-Powered Exam Preparation Agent

A local development project that uses LangGraph workflows, specialized AI agents, and Google OAuth to generate personalized MCQs and evaluate student performance from uploaded syllabi.

## 🚀 Features

### **Core Functionality**
- **AI-Powered MCQ Generation**: Automatically creates multiple-choice questions from PDF/TXT syllabi
- **Specialized Agents**: Math and General subject agents with supervisor delegation
- **Smart Evaluation**: AI-powered exam grading with detailed feedback
- **Google OAuth**: Secure authentication with Google accounts
- **Real-time Workflow**: LangGraph-based processing pipeline
- **Local Development**: Runs entirely on localhost with SQLite database

### **Technical Stack**
- **Backend**: FastAPI, SQLAlchemy, LangGraph
- **AI/ML**: Groq API (Gemma2-9b-it), LangChain
- **Authentication**: Google OAuth 2.0, JWT tokens
- **Database**: SQLite (local development)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **File Processing**: PyPDF2 for PDF text extraction

## 📋 Prerequisites

- Python 3.12+
- Google Cloud Console account (for OAuth setup)
- Groq API key (free tier available)
- Git
- Web browser (Chrome/Firefox recommended for OAuth)

## 🛠️ Installation

> **🏠 For Local Development**: See [LOCAL_SETUP.md](LOCAL_SETUP.md) for a quick 5-minute setup guide

### **1. Clone Repository**
```bash
git clone <repository-url>
cd exam_prep_agent
```

### **2. Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Setup**
Create `.env` file:
```bash
# API Keys (Required)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Google OAuth (Required for login)
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com

# Database (Local SQLite)
DATABASE_URL=sqlite:///./exam_prep.db

# Security (Generate random 32-char string)
SECRET_KEY=your-random-32-character-secret-key

# Optional
LANGCHAIN_API_KEY=lsv2_pt_your_langchain_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=exam-prep-agent
```

### **5. Google OAuth Setup (Local Development)**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Exam Prep Agent Local"
3. Enable **Google Identity** API (not Google+ API)
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Add authorized JavaScript origins:
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`
7. Add authorized redirect URIs:
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`
8. Copy **Client ID** to `.env` file
9. Update `YOUR_GOOGLE_CLIENT_ID` in `exam.html`

### **6. Database Setup**
```bash
# Initialize database
python -c "from app.models.db import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 🚀 Running the Application

### **Start the Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Access Application**
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Agent Health Check**: http://localhost:8000/api/workflow/agent-health

### **Development Features**
- **Hot Reload**: Code changes automatically restart the server
- **Debug Logging**: Detailed logs in console for troubleshooting
- **SQLite Browser**: Easy database inspection with DB Browser for SQLite

## 📖 Usage Guide

### **1. Authentication**
- Click "Sign in with Google" on homepage
- Grant necessary permissions
- Automatic profile creation and login

### **2. Upload Syllabus**
- Support formats: PDF, TXT
- Maximum file size: 10MB
- Automatic topic extraction

### **3. Generate Exam**
- Click "Run Complete Workflow"
- AI agents generate MCQs by topic
- Supervisor coordinates the process

### **4. Take Exam**
- 10 questions per exam session
- Multiple choice format
- Topic-based organization

### **5. View Results**
- Detailed performance analysis
- Question-by-question breakdown
- AI-generated feedback

## 🏗️ Architecture

### **System Components**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   AI Agents     │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   (LangGraph)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite/PG)   │
                       └─────────────────┘
```

### **AI Agent Workflow**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Syllabus   │───►│ Supervisor  │───►│   Math      │
│   Agent     │    │   Agent     │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │  General    │
                   │   Agent     │
                   └─────────────┘
```

### **Database Schema**

```sql
-- Users (Google OAuth)
users: id, email, full_name, google_id, profile_picture, is_premium

-- Syllabi
syllabus: id, title, content, topics, user_id

-- MCQs
mcqs: id, question, option_a, option_b, option_c, option_d, correct_answer, explanation, topic, syllabus_id

-- Quiz Results
quizzes: id, syllabus_id, questions, score, total_questions, user_id
```

## 🔧 API Endpoints

### **Authentication**
```http
POST /api/auth/google          # Google OAuth login
GET  /api/auth/me              # Get current user
```

### **Workflow**
```http
POST /api/syllabus/upload      # Upload syllabus file
POST /api/workflow/prepare-exam/{syllabus_id}  # Generate MCQs
GET  /api/workflow/quiz/{syllabus_id}          # Get quiz questions
POST /api/workflow/submit-exam/{syllabus_id}   # Submit answers
GET  /api/workflow/agent-health                # Check agent status
```

## 🧪 Testing

### **Run Tests**
```bash
pytest tests/ -v
```

### **Test Coverage**
```bash
pytest --cov=app tests/
```

### **Manual Testing**
1. Upload sample PDF syllabus
2. Generate MCQs (should create 15+ questions)
3. Take exam (10 questions)
4. Check evaluation results

## 📊 Monitoring & Logging

### **Logs Location**
- Development: Console output
- Production: `logs/exam_agent.log`

### **Key Metrics**
- MCQ generation success rate
- User authentication rate
- Exam completion rate
- API response times

### **Health Checks**
```bash
curl http://localhost:8000/api/workflow/agent-health
```

## 📊 Performance & Limitations

### **Current Capabilities**
- **File Size**: Up to 10MB PDF/TXT files
- **MCQ Generation**: 3-5 questions per topic
- **Topics**: Up to 20 topics per syllabus
- **Quiz Length**: 10 questions per exam
- **Concurrent Users**: Single user (local development)

### **Response Times**
- **File Upload**: < 5 seconds
- **Topic Extraction**: 5-10 seconds
- **MCQ Generation**: 30-60 seconds (depends on topics)
- **Exam Evaluation**: < 5 seconds

## 🎯 Project Goals

### **Learning Objectives**
- **AI Integration**: Hands-on experience with LangChain and LangGraph
- **Agent Architecture**: Understanding multi-agent systems and delegation
- **OAuth Implementation**: Real-world authentication with Google
- **API Development**: Building RESTful APIs with FastAPI
- **Workflow Orchestration**: Complex multi-step AI processes

### **Technical Achievements**
- **Multi-Agent System**: Supervisor coordinating specialized agents
- **File Processing**: PDF text extraction and analysis
- **Real-time AI**: Streaming responses from Groq API
- **Database Design**: Relational data modeling with SQLAlchemy
- **Frontend Integration**: Vanilla JS with modern OAuth flow

## 🔒 Security (Local Development)

### **Authentication**
- Google OAuth 2.0 integration
- JWT token-based sessions (24-hour expiry)
- Local storage for session persistence

### **Data Protection**
- Input validation on file uploads
- File type restrictions (.pdf, .txt only)
- File size limits (10MB maximum)
- SQL injection prevention with SQLAlchemy ORM

### **Local Security Notes**
- HTTP (not HTTPS) acceptable for localhost
- SQLite database stored locally
- API keys stored in .env file (gitignored)
- No external data transmission except to Groq API

## 🤝 Development Notes

### **Code Structure**
- `app/models/`: Database models (User, Syllabus, MCQ, etc.)
- `app/routes/`: API endpoints (auth, workflow)
- `app/agents/`: AI agents (Supervisor, Math, General, Syllabus)
- `app/auth/`: Authentication handlers (JWT, Google OAuth)
- `app/templates/`: Frontend HTML/CSS/JS
- `app/utils/`: Utility functions (logging, PDF processing)

### **Key Files**
- `main.py`: FastAPI application entry point
- `exam_workflow.py`: LangGraph workflow orchestration
- `supervisor_agent.py`: Agent delegation and coordination
- `exam.html`: Frontend interface
- `.env`: Environment variables (API keys, config)

## 📝 Development Progress

### **Completed Features**
- ✅ Google OAuth authentication
- ✅ AI-powered MCQ generation
- ✅ LangGraph workflow system
- ✅ Supervisor agent delegation
- ✅ Real-time exam evaluation
- ✅ PDF/TXT file processing
- ✅ SQLite database integration
- ✅ RESTful API with FastAPI

### **Potential Enhancements**
- 🔄 Better error handling and user feedback
- 🔄 Mobile responsive design
- 🔄 Bulk syllabus upload
- 🔄 Export results to PDF
- 🔄 Study progress tracking
- 🔄 More question types (True/False, Fill-in-blank)
- 🔄 Custom difficulty levels
- 🔄 Subject-specific agents (Science, History, etc.)

## 🐛 Troubleshooting

### **Common Issues**

**1. Google OAuth Not Working**
```bash
# Check client ID configuration
grep GOOGLE_CLIENT_ID .env
# Verify authorized origins in Google Console
```

**2. MCQ Generation Fails**
```bash
# Check Groq API key
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models
```

**3. Database Connection Error**
```bash
# Reset database
rm exam_prep.db
python -c "from app.models.db import engine, Base; Base.metadata.create_all(bind=engine)"
```

**4. Agent Health Issues**
```bash
# Check agent status
curl http://localhost:8000/api/workflow/agent-health
```

## 📞 Development Resources

### **Documentation**
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Local Setup**: [LOCAL_SETUP.md](LOCAL_SETUP.md) (5-minute quick start)
- **Architecture**: Multi-agent system with LangGraph workflows

### **Useful Links**
- **Groq Console**: https://console.groq.com/ (for API keys)
- **Google Cloud Console**: https://console.cloud.google.com/ (for OAuth setup)
- **LangChain Docs**: https://python.langchain.com/docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

### **Development Tools**
- **DB Browser for SQLite**: View/edit local database
- **Postman/Insomnia**: Test API endpoints
- **Browser DevTools**: Debug frontend and OAuth flow

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 🙏 Acknowledgments

- **LangChain & LangGraph**: Powerful AI agent framework
- **Groq**: Fast and affordable LLM inference
- **FastAPI**: Excellent Python web framework
- **Google OAuth**: Secure authentication service
- **SQLAlchemy**: Robust Python ORM

## 🎆 Learning Outcomes

This project demonstrates:
- **Multi-agent AI systems** with specialized roles
- **Workflow orchestration** using LangGraph
- **Modern web APIs** with FastAPI
- **OAuth 2.0 implementation** with Google
- **File processing** and text extraction
- **Database design** and ORM usage
- **Frontend-backend integration**

---

**Built for learning AI agent development and workflow orchestration 🤖**