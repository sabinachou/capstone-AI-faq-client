# AI-Powered FAQ System

A modern, intelligent FAQ system powered by OpenAI GPT that provides smart answers, session management, and comprehensive analytics. Built with Flask (backend) and React (frontend).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

### AI-Powered Intelligence
- **Smart Chat**: OpenAI GPT-3.5 integration for intelligent responses
- **Semantic Understanding**: Advanced text processing and keyword extraction
- **Context Awareness**: Multi-turn conversations with session management
- **Confidence Scoring**: AI confidence levels for answer quality assessment
- **Hybrid Strategy**: FAQ matching combined with AI generation

### Analytics & Management
- **Real-time Analytics**: Question trends, category statistics, and usage metrics
- **Session Tracking**: Complete conversation history and user journey mapping
- **CSAT Scoring**: Customer satisfaction tracking and feedback collection
- **User Management**: Registration, authentication, and user profiles
- **Admin Dashboard**: Comprehensive system monitoring and management

### Technical Features
- **RESTful API**: Complete API suite with 15+ endpoints
- **Database Integration**: SQLite/PostgreSQL support with automatic migrations
- **Security**: JWT authentication, input validation, and rate limiting
- **Scalable Architecture**: Modular design for easy extension and maintenance
- **Production Ready**: Docker support, logging, and error handling

## How to run and test

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/AI-faq-client.git
   cd AI-faq-client
   ```

2. **Backend Setup**
   ```bash
   cd faq-backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Start Backend Server**
   ```bash
   python app.py
   # Server runs on http://localhost:5000
   ```

5. **Frontend Setup**
   ```bash
   cd ../faq-frontend
   npm install
   npm start
   # Frontend runs on http://localhost:3000
   ```

## Documentation

### API Endpoints

#### Chat & AI
- `POST /api/chat` - Intelligent chat with AI
- `POST /api/feedback` - Submit user feedback

#### Session Management
- `POST /api/session/start` - Start new conversation session
- `POST /api/session/end` - End active session
- `GET /api/session/status/<id>` - Get session status
- `GET /api/session/questions/<id>` - Get session history

#### Analytics
- `GET /api/top-questions` - Most frequently asked questions
- `GET /api/categories` - Question categories
- `GET /api/daily-question-counts` - Daily usage statistics
- `GET /api/csat` - Customer satisfaction scores

#### User Management
- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `POST /api/logout` - User logout
- `GET /api/current-user` - Get current user info

#### FAQ Management
- `GET /api/faqs` - Get all FAQs
- `POST /api/faqs` - Create new FAQ
- `PUT /api/faqs` - Update existing FAQ
- `DELETE /api/faqs` - Delete FAQ

### Example Usage

**Send a question to AI**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I reset my password?",
    "session_id": "optional-session-id"
  }'
```

**Response**
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

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Flask Backend │    │   OpenAI API    │
│                 │    │                 │    │                 │
│ • User Interface│◄──►│ • REST API      │◄──►│ • GPT-3.5       │
│ • State Mgmt    │    │ • Session Mgmt  │    │ • Text Analysis │
│ • HTTP Client   │    │ • AI Integration│    │ • Generation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite/PG DB  │
                       │                 │
                       │ • FAQs          │
                       │ • Sessions      │
                       │ • Users         │
                       │ • Analytics     │
                       └─────────────────┘
```

## Configuration

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# AI Parameters
AI_SIMILARITY_THRESHOLD=0.3
AI_MAX_TOKENS=500
AI_TEMPERATURE=0.7
AI_CONFIDENCE_HIGH=0.8
AI_CONFIDENCE_MEDIUM=0.5

# Database
DATABASE_URL=sqlite:///faq.db

# Security
SECRET_KEY=your-secret-key
SESSION_TIMEOUT=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### AI Model Tuning

- **Similarity Threshold**: Lower values increase recall but may reduce precision
- **Temperature**: Controls creativity (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Limits response length
- **Confidence Levels**: Thresholds for answer quality classification

## Testing

### Run Tests
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
  -d '{"question": "Test question"}'

# Test session management
curl -X POST http://localhost:5000/api/session/start
```

## Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Production Setup
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Environment setup
export FLASK_ENV=production
export DEBUG=False
```

### Nginx Configuration
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

## Monitoring

### Key Metrics
- Response time and throughput
- AI confidence scores and accuracy
- User satisfaction (CSAT) ratings
- Session duration and engagement
- Error rates and system health

### Logging
```bash
# View application logs
tail -f app.log

# Monitor API usage
grep "POST /api/chat" app.log | wc -l

# Check for errors
grep "ERROR" app.log | tail -20
```



## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [React](https://reactjs.org/) for the frontend framework
- [scikit-learn](https://scikit-learn.org/) for machine learning utilities

## Support

If you encounter any issues or have questions:

1. Check the [AI Setup Guide](AI_SETUP_GUIDE.md) for detailed configuration
2. Review the [API Documentation](API_list.md) for endpoint details
3. Search existing [Issues](https://github.com/your-username/AI-faq-client/issues)
4. Create a new issue with detailed information

## Roadmap

- [ ] Multi-language support
- [ ] Voice input/output capabilities
- [ ] Advanced analytics dashboard
- [ ] Integration with popular chat platforms
- [ ] Machine learning model fine-tuning
- [ ] Real-time collaboration features
- [ ] Mobile app development

