# 🎓 AI-Powered Exam Preparation Agent

An intelligent exam preparation system that uses LangGraph workflows, specialized AI agents, and Google OAuth to generate personalized MCQs and evaluate student performance.

## 🚀 Features

### **Core Functionality**
- **AI-Powered MCQ Generation**: Automatically creates multiple-choice questions from uploaded syllabi
- **Specialized Agents**: Math and General subject agents with supervisor delegation
- **Smart Evaluation**: AI-powered exam grading with detailed feedback
- **Google OAuth**: Secure authentication with Google accounts
- **Real-time Workflow**: LangGraph-based processing pipeline

### **Technical Stack**
- **Backend**: FastAPI, SQLAlchemy, LangGraph
- **AI/ML**: Groq API (Gemma2-9b-it), LangChain
- **Authentication**: Google OAuth 2.0, JWT tokens
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment**: Docker, Docker Compose

## 📋 Prerequisites

- Python 3.12+
- Google Cloud Console account
- Groq API key
- Git

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

### **Development**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Production (Docker)**
```bash
docker-compose up -d
```

### **Access Application**
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/workflow/agent-health

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

## 🚀 Production Deployment

### **Infrastructure Requirements**
- **CPU**: 4 cores minimum
- **RAM**: 8GB minimum
- **Storage**: 50GB SSD
- **Network**: 1Gbps

### **Environment Setup**
```bash
# Production environment variables
DATABASE_URL=postgresql://user:pass@host:5432/examdb
REDIS_URL=redis://host:6379
GOOGLE_CLIENT_ID=prod-client-id
SECRET_KEY=256-bit-production-key
```

### **Docker Deployment**
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Database migrations
docker exec app alembic upgrade head

# Monitor logs
docker logs -f app
```

### **Scaling Strategy**
- **Load Balancer**: Nginx/CloudFlare
- **App Servers**: 3+ FastAPI instances
- **Database**: PostgreSQL with read replicas
- **Cache**: Redis cluster
- **Background Jobs**: Celery workers

## 💰 Business Model

### **Pricing Tiers**
- **Free**: 5 exams/month
- **Premium**: $9.99/month unlimited
- **Enterprise**: Custom pricing

### **Revenue Projections**
- **Year 1**: $60K ARR (500 paid users)
- **Year 2**: $300K ARR (2,500 paid users)
- **Year 3**: $1M ARR (8,000 paid users)

## 🔒 Security

### **Authentication**
- Google OAuth 2.0 integration
- JWT token-based sessions
- Secure token storage

### **Data Protection**
- Input validation on all endpoints
- File upload restrictions
- Rate limiting (100 requests/hour)
- HTTPS enforcement in production

### **Privacy**
- User data encrypted at rest
- No password storage required
- GDPR compliant data handling

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

### **Code Standards**
- Python: PEP 8 compliance
- JavaScript: ES6+ standards
- Documentation: Docstrings required
- Testing: 80%+ coverage

## 📝 Changelog

### **v1.0.0** (Current)
- ✅ Google OAuth authentication
- ✅ AI-powered MCQ generation
- ✅ LangGraph workflow system
- ✅ Supervisor agent delegation
- ✅ Real-time exam evaluation

### **Roadmap v1.1.0**
- 🔄 Payment integration (Stripe)
- 🔄 Mobile responsive design
- 🔄 Bulk syllabus upload
- 🔄 Performance analytics

### **Roadmap v1.2.0**
- 🔄 Mobile app (React Native)
- 🔄 Collaborative study groups
- 🔄 AI study recommendations
- 🔄 Offline mode support

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

## 📞 Support

### **Documentation**
- API Docs: http://localhost:8000/docs
- Architecture: `/docs/architecture.md`
- Deployment: `/PRODUCTION_GUIDE.md`

### **Community**
- GitHub Issues: Bug reports and features
- Discussions: General questions
- Wiki: Extended documentation

### **Commercial Support**
- Email: support@examprep.ai
- Response Time: 24 hours
- SLA: 99.9% uptime guarantee

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: AI agent framework
- **Groq**: Fast LLM inference
- **FastAPI**: Modern Python web framework
- **Google**: OAuth authentication service

---

**Built with ❤️ for better education through AI**