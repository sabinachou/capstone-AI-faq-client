# AI Intelligent FAQ System Setup Guide

This comprehensive guide will help you set up and deploy an AI-powered FAQ system with intelligent answering capabilities, session management, and analytics.

## 🚀 System Features

### Core AI Capabilities
- **Intelligent Chat**: OpenAI GPT-powered conversational AI
- **Semantic Understanding**: Advanced text processing and keyword extraction
- **Context Awareness**: Session-based conversation management
- **Emotion Recognition**: Sentiment analysis for user interactions
- **Smart Matching**: TF-IDF vectorization and cosine similarity for FAQ matching

### Advanced Features
- ✅ Multi-turn conversation support with session management
- ✅ Real-time analytics and reporting
- ✅ User authentication and management
- ✅ Feedback collection and CSAT scoring
- ✅ Category-based question organization
- ✅ Daily usage statistics and trends
- ✅ RESTful API with comprehensive endpoints

## 📋 System Requirements

### Backend Requirements
- **Python**: 3.8 or higher
- **Flask**: 3.0.0
- **Database**: SQLite (included) or PostgreSQL
- **AI Service**: OpenAI API account
- **Memory**: Minimum 2GB RAM
- **Storage**: 1GB available space

### Frontend Requirements
- **Node.js**: 16.0 or higher
- **React**: 18.0 or higher
- **Browser**: Modern browsers (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation Guide

### 1. Environment Setup

#### Clone the Repository
```bash
git clone <repository-url>
cd AI-faq-client
```

#### Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Backend Configuration

#### Install Dependencies
```bash
cd faq-backend
pip install -r requirements.txt
```

#### Environment Variables Setup
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
nano .env
```

**Required Environment Variables:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# AI Service Parameters
AI_SIMILARITY_THRESHOLD=0.3
AI_MAX_TOKENS=500
AI_TEMPERATURE=0.7
AI_CONFIDENCE_HIGH=0.8
AI_CONFIDENCE_MEDIUM=0.5

# Database Configuration
DATABASE_URL=sqlite:///faq.db

# Security
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

#### Initialize Database
```bash
python app.py
# Database will be automatically created on first run

# Optional: Load sample data
python sample_faqs.py
```

#### Start Backend Server
```bash
python app.py
# Server will start on http://localhost:5000
```

### 3. Frontend Setup

```bash
cd faq-frontend
npm install
npm start
# Frontend will start on http://localhost:3000
```

## 🔧 API Documentation

### Core Chat API

**Intelligent Chat Endpoint**
```http
POST /api/chat
Content-Type: application/json

{
  "question": "How do I reset my password?",
  "session_id": "optional-session-id"
}
```

**Response Format**
```json
{
  "answer": "To reset your password, go to the IT self-service portal...",
  "confidence": 0.95,
  "source": "FAQ",
  "keywords": ["password", "reset", "IT"],
  "category": "IT Support",
  "session_id": "session-uuid"
}
```

### Session Management APIs

**Start Session**
```http
POST /api/session/start
{
  "user_id": "optional-user-id"
}
```

**End Session**
```http
POST /api/session/end
{
  "session_id": "session-uuid"
}
```

**Session Status**
```http
GET /api/session/status/<session_id>
```

### Analytics APIs

**Top Questions**
```http
GET /api/top-questions
```

**Category Statistics**
```http
GET /api/categories
GET /api/category-details/<category>
```

**Daily Metrics**
```http
GET /api/daily-question-counts
GET /api/csat
```

### User Management APIs

**User Registration**
```http
POST /api/register
{
  "username": "john_doe",
  "email": "john@company.com",
  "password": "secure_password"
}
```

**User Login**
```http
POST /api/login
{
  "username": "john_doe",
  "password": "secure_password"
}
```

## 🎯 AI System Workflow

### 1. Question Processing Pipeline
```
User Input → Text Preprocessing → Keyword Extraction → Semantic Analysis
     ↓              ↓                    ↓                ↓
Session Check → FAQ Matching → AI Enhancement → Response Generation
```

### 2. Decision Logic

**High Confidence (>0.8)**
- Direct FAQ match found
- Return exact FAQ answer
- Source: "FAQ"

**Medium Confidence (0.5-0.8)**
- Partial FAQ match
- AI enhances with context
- Source: "AI_Enhanced"

**Low Confidence (<0.5)**
- No relevant FAQ found
- Pure AI generation
- Source: "AI_Generated"

### 3. Session Management
- Automatic session creation for new conversations
- Context preservation across multiple questions
- Session timeout handling (default: 1 hour)
- Question history tracking

## ⚙️ Configuration & Optimization

### AI Model Tuning

**Similarity Threshold**
```env
# Lower values increase recall but may reduce precision
AI_SIMILARITY_THRESHOLD=0.3
```

**Response Generation**
```env
# Control response length
AI_MAX_TOKENS=500

# Control creativity (0.0 = deterministic, 1.0 = creative)
AI_TEMPERATURE=0.7
```

**Confidence Levels**
```env
# Adjust confidence thresholds
AI_CONFIDENCE_HIGH=0.8
AI_CONFIDENCE_MEDIUM=0.5
```

### Performance Optimization

**Caching Strategy**
- FAQ vectors cached in memory
- Session data cached for quick access
- Common questions cached for faster responses

**Database Optimization**
```sql
-- Add indexes for better performance
CREATE INDEX idx_faq_question ON faq(question);
CREATE INDEX idx_log_timestamp ON log(timestamp);
CREATE INDEX idx_session_active ON conversation_session(is_active);
```

## 🧪 Testing & Validation

### Run Test Suite
```bash
# Backend tests
cd faq-backend
python -m pytest test_*.py -v

# Specific test modules
python test_ai_service.py
python test_keyword_service.py
python test_session_integration.py
```

### API Testing
```bash
# Test chat functionality
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'

# Test session management
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 🚨 Troubleshooting

### Common Issues

**1. OpenAI API Errors**
```bash
# Check API key validity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Verify account balance
# Check rate limits and quotas
```

**2. Database Connection Issues**
```bash
# Check database file permissions
ls -la faq.db

# Recreate database if corrupted
rm faq.db
python app.py
```

**3. Session Management Problems**
```bash
# Clear session data
rm -rf flask_session/

# Check session timeout settings
grep SESSION_TIMEOUT .env
```

**4. Performance Issues**
```bash
# Monitor memory usage
top -p $(pgrep -f "python app.py")

# Check log file size
ls -lh app.log

# Rotate logs if needed
mv app.log app.log.old
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python app.py

# Monitor real-time logs
tail -f app.log | grep ERROR
```

## 📊 Monitoring & Analytics

### Key Metrics
- **Response Time**: Average API response time
- **Accuracy**: User satisfaction scores (CSAT)
- **Usage**: Daily question counts and trends
- **Categories**: Most popular question categories
- **Sessions**: Active sessions and duration

### Log Analysis
```bash
# View recent errors
grep "ERROR" app.log | tail -20

# Analyze API usage
grep "POST /api/chat" app.log | wc -l

# Check session statistics
grep "session" app.log | tail -10
```

## 🔐 Security Best Practices

### API Security
- Store API keys in environment variables
- Use HTTPS in production
- Implement rate limiting
- Validate all user inputs
- Sanitize database queries

### Session Security
- Use secure session cookies
- Implement session timeout
- Validate session tokens
- Log security events

### Data Protection
- Encrypt sensitive data
- Regular database backups
- Access control and authentication
- Audit trail logging

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
export FLASK_ENV=production
export DEBUG=False
export LOG_LEVEL=WARNING

# Use production database
export DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Web Server Configuration
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📞 Support & Maintenance

### Regular Maintenance
- Monitor API usage and costs
- Update dependencies regularly
- Backup database weekly
- Review and rotate logs
- Update FAQ content

### Performance Monitoring
- Set up alerts for high error rates
- Monitor response times
- Track user satisfaction scores
- Analyze usage patterns

### Getting Help
For technical support, please provide:
- Error logs and stack traces
- System configuration details
- Steps to reproduce the issue
- Expected vs actual behavior

---

**Important**: Ensure your OpenAI API key is properly configured and has sufficient credits before deploying to production. The system will gracefully degrade to FAQ-only mode if AI services are unavailable.