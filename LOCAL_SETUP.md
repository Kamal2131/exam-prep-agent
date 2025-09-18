# 🏠 Local Development Setup Guide

## 🚀 Quick Start (5 Minutes)

### **Step 1: Get Groq API Key**
1. Go to [Groq Console](https://console.groq.com/)
2. Sign up/Login with Google
3. Go to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_`)

### **Step 2: Setup Google OAuth**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Create New Project**: "Exam Prep Local"
3. **Enable API**: Search "Google Identity" → Enable
4. **Create Credentials**:
   - Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
   - Application type: **Web application**
   - Name: "Exam Prep Local"
   - **Authorized JavaScript origins**: `http://localhost:8000`
   - **Authorized redirect URIs**: `http://localhost:8000`
5. **Copy Client ID** (looks like: `123456789-abc...apps.googleusercontent.com`)

### **Step 3: Create Environment File**
Create `.env` file in project root:
```bash
# Replace with your actual keys
GROQ_API_KEY=gsk_your_actual_groq_key_here
GOOGLE_CLIENT_ID=your_actual_google_client_id_here

# Local database
DATABASE_URL=sqlite:///./exam_prep.db

# Generate random 32-character string
SECRET_KEY=abcd1234efgh5678ijkl9012mnop3456

# Optional (for debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=exam-prep-local
```

### **Step 4: Update Frontend**
Edit `app/templates/exam.html` line ~30:
```html
<!-- Replace YOUR_GOOGLE_CLIENT_ID with your actual Client ID -->
<div id="g_id_onload"
     data-client_id="123456789-abc...apps.googleusercontent.com"
     data-callback="handleCredentialResponse">
</div>
```

### **Step 5: Install & Run**
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.models.db import engine, Base; Base.metadata.create_all(bind=engine)"

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 6: Test**
1. Open: http://localhost:8000
2. Click "Sign in with Google"
3. Upload a PDF/TXT file
4. Generate exam and test!

## 🔧 Troubleshooting

### **Google OAuth Issues**
```bash
# Error: "redirect_uri_mismatch"
# Solution: Add http://localhost:8000 to authorized origins in Google Console

# Error: "invalid_client"
# Solution: Check GOOGLE_CLIENT_ID in .env matches Google Console

# Error: "access_blocked"
# Solution: Make sure project is not in testing mode or add your email as test user
```

### **API Key Issues**
```bash
# Error: "Invalid API key"
# Solution: Check GROQ_API_KEY in .env file

# Error: "Rate limit exceeded"
# Solution: Wait a few minutes or upgrade Groq plan
```

### **Database Issues**
```bash
# Reset database if corrupted
rm exam_prep.db
python -c "from app.models.db import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 📱 Local Testing Checklist

- [ ] Google login works
- [ ] File upload works (PDF/TXT)
- [ ] MCQ generation works (15+ questions)
- [ ] Quiz display works (10 questions)
- [ ] Exam submission works
- [ ] Results display correctly
- [ ] Agent health check passes

## 🎯 Sample Test Files

Create these test files to verify functionality:

**test_syllabus.txt**:
```
Mathematics Syllabus
1. Algebra - Linear equations, quadratic equations
2. Geometry - Triangles, circles, area calculations
3. Statistics - Mean, median, mode, probability
```

**Expected Results**:
- 3 topics extracted
- 9-15 MCQs generated
- 10 questions in quiz
- Detailed evaluation with feedback

## 🚀 Next Steps

Once local setup works:
1. **Add more subjects** - Upload different syllabi
2. **Test edge cases** - Large files, complex topics
3. **Customize UI** - Modify templates/exam.html
4. **Add features** - Progress tracking, study notes
5. **Deploy to cloud** - Follow PRODUCTION_GUIDE.md

## 💡 Development Tips

### **Hot Reload**
```bash
# Auto-restart on code changes
uvicorn app.main:app --reload
```

### **Debug Mode**
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

### **Database Inspection**
```bash
# View database contents
sqlite3 exam_prep.db
.tables
SELECT * FROM users;
SELECT * FROM mcqs LIMIT 5;
```

### **API Testing**
```bash
# Test endpoints directly
curl http://localhost:8000/api/workflow/agent-health
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/auth/me
```

## 🔒 Security Notes

### **Local Development Only**
- HTTP (not HTTPS) is OK for localhost
- SQLite database is fine for testing
- No SSL certificates needed
- Rate limiting disabled in development

### **Don't Commit Secrets**
Add to `.gitignore`:
```
.env
exam_prep.db
logs/
__pycache__/
```

## 📞 Need Help?

### **Common Solutions**
1. **Port already in use**: Change port with `--port 8001`
2. **Permission denied**: Run with `sudo` on Linux/Mac
3. **Module not found**: Activate virtual environment first
4. **Google OAuth fails**: Check browser console for errors

### **Get Support**
- Check logs in terminal
- Test API endpoints with curl
- Verify environment variables
- Clear browser cache/cookies

---

**🎉 You're ready to build AI-powered exams locally!**