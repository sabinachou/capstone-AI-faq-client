# AI-Powered FAQ System - Demo Video Script

**Duration:** ~10 minutes  
**Focus:** Full-stack integration, REST API testing, and problem-solving

---

## Introduction (1 minute)

**[Screen: GitHub Repository]**

"Hello! Welcome to our group's capstone project demonstration. I'm excited to show you our AI FAQ System - a full-stack application that combines AI responses with comprehensive analytics and user management.

This project has the integration of a React frontend with a Flask backend through REST APIs, featuring OpenAI  integration, real-time analytics, and session management. Let me walk you through the complete system and show you how the frontend and backend work together "

**[Screen: Project Structure Overview]**

---

## System Architecture & API Overview (2 minutes)

**[Screen: API Documentation]**

"Let me start by showing you the REST API architecture that connects our frontend and backend. Our system provides four main API categories:

1. **Chat & AI APIs** - The core intelligence of our system
   - `/api/chat` for AI-powered conversations
   - `/api/feedback` for user satisfaction tracking

2. **Session Management APIs** - For conversation tracking
   - `/api/session/start` and `/api/session/end` for session lifecycle
   - `/api/session/status` and `/api/session/questions` for session monitoring

3. **Analytics APIs** - For data insights
   - `/api/top-questions` for trending topics
   - `/api/categories` for question categorization
   - `/api/daily-question-counts` for usage statistics

4. **User Management APIs** - For authentication and user profiles
   - `/api/register`, `/api/login`, `/api/logout` for user authentication

---

## Backend Demonstration (2.5 minutes)

**[Screen: Terminal - Backend Setup]**

"Let me demonstrate the backend functionality. First, I'll start the Flask server:"

```bash
cd faq-backend
python app.py
```

"The server is now running on localhost:5000. Let me test some key API endpoints using curl commands to show the REST API functionality."

**[Screen: Terminal - API Testing]**

"First, let's test the chat API - the heart of our AI system:"

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?", "session_id": "demo_session"}'
```

"As you can see, the API returns an intelligent response with confidence scoring and source attribution. The AI successfully processes the question and provides a relevant answer.

Now let's test session management:"

```bash
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user"}'
```

"Perfect! We get a session ID that we can use to track the conversation. Let's check our analytics:"

```bash
curl http://localhost:5000/api/top-questions
```

"The analytics API shows us the most frequently asked questions with categorization and count data. This demonstrates how our backend processes and stores interaction data for insights."

---

## Frontend Demonstration (2.5 minutes)

**[Screen: Terminal - Frontend Setup]**

"Now let's see how the React frontend integrates with these APIs. Starting the frontend:"

```bash
cd faq-frontend
npm start
```

**[Screen: Browser - Login Page]**

"The application opens to our login page. This shows the user authentication flow using our `/api/login` endpoint. Let me log in as a demo user."

**[Action: Login with demo credentials]**

**[Screen: Browser - Chat Interface]**

"Here's our main chat interface. This is where users interact with the AI system. Let me ask a question to demonstrate the frontend-backend integration:"

**[Action: Type and send a question]**

"Watch how the frontend makes a POST request to `/api/chat`, processes the response, and displays the AI-generated answer with confidence scoring. The session is automatically managed through our session APIs.

**[Screen: Browser - Admin Dashboard]**

"Now let's look at the admin dashboard, which shows the analytics APIs in action. This page pulls data from multiple endpoints:"

**[Action: Navigate through analytics]**

"The dashboard displays:
- Top questions from `/api/top-questions`
- Category statistics from `/api/categories`
- Daily usage trends from `/api/daily-question-counts`
- Session statistics from `/api/session/statistics`

All this data is fetched in real-time and presented in an intuitive interface."

---

## Challenges and Solutions (1.5 minutes)

**[Screen: Code Editor - Problem Areas]**

"During development, I encountered some chanllenges that I'd like to share:

**Problem: AI Service Unavailable Error**
When testing the chat functionality, I encountered an AI service error that prevented the system from responding to user questions.

**Investigation Process:**
After troubleshooting, I discovered the root cause:
- The `ai_service.py` file was missing environment variable loading
- This led to a specific error: 'The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()'
- This was a numpy array comparison issue that needed to be addressed in the AI service logic

**Technical Details:**
The error occurred due to improper numpy array comparison in the smart_answer function's conditional statements. When comparing numpy arrays directly in boolean contexts, Python cannot determine the truth value of arrays with multiple elements.

**Solution Implementation:**
I fixed the error by modifying the conditional judgment logic in the smart_answer function within `ai_service.py`. This involved:
- Adding proper environment variable loading
- Correcting the array comparison logic using appropriate numpy methods
- Ensuring the AI service could handle array operations correctly

**Result:**
The API now responds normally to user questions and returns intelligently generated answers. The AI service is fully functional and provides reliable responses to user queries."

---


## Conclusion (0.5 minutes)

**[Screen: GitHub Repository]**

"In summary, I've successfully created a full-stack AI-powered FAQ system that demonstrates:

✅ **Complete REST API Integration** - 15+ endpoints connecting React frontend with Flask backend
✅ **Real-time AI Functionality** - OpenAI GPT integration with session management
✅ **Comprehensive Analytics** - Data visualization and user insights
✅ **Robust Error Handling** - Graceful failure management and user feedback
✅ **Production-Ready Code** - Proper testing, documentation, and deployment configuration

The entire codebase, documentation, and setup instructions are available in the GitHub repository. Thank you for watching this demonstration of my capstone project!"

