# backend APIs
# This file contains the Flask application for the FAQ API.
# It includes endpoints to get, add, update, and delete FAQs.
# Updated for PostgreSQL deployment on Azure

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask import session
from config import Config
from models import db, FAQ, Log, Feedback, User, ConversationSession
from ai_service import ai_service
from keyword_service import keyword_service
from conversation_service import conversation_service

from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from datetime import timedelta, datetime
import os
import logging

# Configure logging for Azure deployment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS to allow frontend access
CORS(app, 
     supports_credentials=True,
     origins=[
         "http://localhost:3000",  # 本地开发
         "https://purple-bay-044a4fe1e-preview.westus2.1.azurestaticapps.net",  # Azure前端
         "https://*.azurestaticapps.net",  # 所有Azure Static Web Apps
         "https://*.azurewebsites.net"     # 所有Azure Web Apps
     ],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     expose_headers=["Set-Cookie", "Access-Control-Allow-Credentials"],
     max_age=3600)  # 缓存预检请求结果1小时

app.config.from_object(Config)

# 配置Session以确保在Azure环境中正常工作
app.config.update(
    SESSION_COOKIE_SECURE=True,  # 在HTTPS下使用
    SESSION_COOKIE_HTTPONLY=True,  # 防止XSS攻击
    SESSION_COOKIE_SAMESITE='None',  # 允许跨站请求（Azure部署需要）
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),  # session有效期24小时
    SESSION_COOKIE_DOMAIN=None,  # 允许跨子域名访问
    SESSION_COOKIE_PATH='/',  # 确保cookie在所有路径下可用
    SESSION_REFRESH_EACH_REQUEST=True  # 每次请求都刷新session
)

# 如果不在HTTPS环境（如本地开发），禁用secure cookie
if app.config.get('FLASK_ENV') == 'development':
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 添加认证中间件
@app.before_request
def handle_preflight():
    """Handle preflight requests for CORS"""
    if request.method == 'OPTIONS':
        response = make_response()
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With'
            response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
            response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie,Access-Control-Allow-Credentials'
            response.headers['Access-Control-Max-Age'] = '3600'
        return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    origin = request.headers.get('Origin')
    if origin:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Expose-Headers'] = 'Set-Cookie,Access-Control-Allow-Credentials'
        
        # 确保Set-Cookie头部正确设置
        if 'Set-Cookie' in response.headers:
            # 修改cookie设置以支持跨域
            cookies = response.headers.getlist('Set-Cookie')
            new_cookies = []
            for cookie in cookies:
                if 'SameSite' not in cookie:
                    cookie += '; SameSite=None'
                if 'Secure' not in cookie:
                    cookie += '; Secure'
                new_cookies.append(cookie)
            response.headers.setlist('Set-Cookie', new_cookies)
    
    return response

# initialize the database
db.init_app(app)

# Initialize database with PostgreSQL compatibility
def init_database():
    """Initialize database with PostgreSQL compatibility"""
    try:
        with app.app_context():
            # Test database connection with retry logic
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    # Test database connection
                    db.session.execute(text('SELECT 1'))
                    db.session.commit()
                    logger.info("Database connection successful")
                    break
                except OperationalError as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"Database connection failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"Database connection attempt {retry_count} failed, retrying... Error: {e}")
                    import time
                    time.sleep(2 ** retry_count)  # Exponential backoff
            
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

# Initialize database on startup
try:
    init_database()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    # In production, you might want to exit here
    # import sys
    # sys.exit(1)

# Database connection health check
def check_db_connection():
    """Check if database connection is healthy"""
    try:
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

# get all FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    try:
        if not check_db_connection():
            return jsonify({"error": "Database connection unavailable"}), 503
            
        faqs = FAQ.query.all()
        return jsonify([faq.to_dict() for faq in faqs]), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_faqs: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_faqs: {e}")
        return jsonify({"error": "Internal server error"}), 500


# get specific FAQ by ID
@app.route('/api/faqs/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    faq = FAQ.query.get(faq_id)
    if faq:
        return jsonify(faq.to_dict()), 200
    return jsonify({"error": "FAQ not found"}), 404


# add a new FAQ
@app.route('/api/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    try:
        if not data or "question" not in data or "answer" not in data:
            return jsonify({"error": "Both question and answer are required"}), 400

        # 单条插入
        if not isinstance(data, list):
            new_faq = FAQ(question=data["question"], answer=data["answer"])
            db.session.add(new_faq)
            db.session.commit()
            return jsonify(new_faq.to_dict()), 201
        # 批量插入
        else:
            new_faqs = []
            for item in data:
                if "question" in item and "answer" in item:
                    new_faq = FAQ(question=item["question"], answer=item["answer"])
                    db.session.add(new_faq)
                    new_faqs.append(new_faq.to_dict())
            db.session.commit()
            return jsonify(new_faqs), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# update an existing FAQ
@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    faq = FAQ.query.get(faq_id)
    if not faq:
        return jsonify({"error": "FAQ not found"}), 404

    data = request.get_json()
    if "question" in data:
        faq.question = data["question"]
    if "answer" in data:
        faq.answer = data["answer"]

    db.session.commit()
    return jsonify(faq.to_dict()), 200


# delete a FAQ
@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    faq = FAQ.query.get(faq_id)
    if faq:
        db.session.delete(faq)
        db.session.commit()
        return jsonify({"message": "FAQ deleted successfully"}), 200
    return jsonify({"error": "FAQ not found"}), 404

# check if the server is running
@app.route('/')
def index():
    return jsonify({"message": "FAQ API is running"}), 200

# Log a question
@app.route('/api/log', methods=['POST'])
def log_question():
    data = request.get_json()
    question = data.get('question')
    if question:
        log = Log(question=question)
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Logged'}), 201
    return jsonify({'error': 'No question provided'}), 400

# Get top 5 most asked question categories
@app.route('/api/top-questions')
def top_questions():
    # Count questions by category
    results = db.session.query(
        Log.category, func.count().label('count')
    ).filter(Log.category.isnot(None))\
     .group_by(Log.category)\
     .order_by(func.count().desc())\
     .limit(5).all()

    return jsonify([{'question': category, 'count': count} for category, count in results])

# Get questions by category
@app.route('/api/category-details/<category>')
def category_details(category):
    questions = db.session.query(
        Log.question, Log.keywords, Log.timestamp
    ).filter(Log.category == category)\
     .order_by(Log.timestamp.desc())\
     .limit(20).all()
    
    return jsonify([
        {
            'question': q,
            'keywords': k,
            'timestamp': t.isoformat() if t else None
        } for q, k, t in questions
    ])

# Get all categories with counts
@app.route('/api/categories')
def get_categories():
    results = db.session.query(
        Log.category, func.count().label('count')
    ).filter(Log.category.isnot(None))\
     .group_by(Log.category)\
     .order_by(func.count().desc())\
     .all()
    
    return jsonify([{'category': category, 'count': count} for category, count in results])

# Get daily question counts for the last 7 days
@app.route('/api/daily-question-counts')
def daily_counts():
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)

    results = db.session.query(
        func.date(Log.timestamp),
        func.count()
    ).filter(Log.timestamp >= start_date)\
     .group_by(func.date(Log.timestamp))\
     .order_by(func.date(Log.timestamp))\
     .all()

    return jsonify([{'date': str(d), 'count': c} for d, c in results])

# Submit feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = Feedback(satisfied=data['satisfied'])
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback received"}), 201

# Get CSAT score
@app.route('/api/csat')
def get_csat():
    total = db.session.query(func.count(Feedback.id)).scalar()
    if total == 0:
        return jsonify({'csat': 0})
    
    satisfied_count = db.session.query(func.count(Feedback.id))\
                        .filter(Feedback.satisfied == True).scalar()
    
    csat_score = round((satisfied_count / total) * 100, 2)
    return jsonify({'csat': csat_score})



# AI Chat API Endpoint
@app.route('/api/chat', methods=['POST'])
def smart_chat():
    data = request.get_json()
    user_question = data.get('question', '').strip()
    session_id = data.get('session_id')  # Optional session ID
    
    if not user_question:
        return jsonify({'error': 'Question cannot be empty'}), 400
    
    try:
        # Extract keywords and classification
        keyword_result = keyword_service.process_question(user_question)
        
        # If session_id is provided, verify if session is active
        session_active = False
        if session_id:
            session_active = conversation_service.is_session_active(session_id)
            if session_active:
                conversation_service.update_session_activity(session_id)
        
        # Log user question with keywords, category and session info
        log = Log(
            question=user_question,
            keywords=keyword_result['keywords_str'],
            category=keyword_result['category'],
            session_id=session_id if session_active else None
        )
        db.session.add(log)
        db.session.commit()
        
        # Get all FAQs
        faqs = FAQ.query.all()
        
        # Use AI service to generate intelligent answer
        result = ai_service.smart_answer(user_question, faqs)
        
        response_data = {
            'question': user_question,
            'answer': result['answer'],
            'source': result['source'],
            'confidence': result['confidence'],
            'similarity': result.get('similarity', 0.0),
            'emotion_analysis': result.get('emotion_analysis', {}),
            'requires_human': result.get('requires_human', False)
        }
        
        # If there's an active session, add session information
        if session_active:
            response_data['session_id'] = session_id
            response_data['session_active'] = True
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Intelligent Chat API Error: {e}")
        return jsonify({
            'question': user_question,
            'answer': 'Sorry, the service is temporarily unavailable. Please try again later.',
            'source': 'error',
            'confidence': 'low',
            'similarity': 0.0
        }), 500

# User Authentication APIs
# Session management API endpoints
@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Start a new conversation session"""
    data = request.get_json() or {}
    user_id = session.get('user_id')  # Get user ID from current login session
    
    result = conversation_service.start_session(user_id)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 500

@app.route('/api/session/end', methods=['POST'])
def end_session():
    """End conversation session and submit feedback"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'error': 'Session ID is required'}), 400
    
    # Extract feedback data
    feedback_data = None
    if any(key in data for key in ['satisfied', 'rating', 'comment']):
        feedback_data = {
            'satisfied': data.get('satisfied', True),
            'rating': data.get('rating'),
            'comment': data.get('comment', '').strip() or None
        }
    
    result = conversation_service.end_session(session_id, feedback_data)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@app.route('/api/session/status/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get session status"""
    is_active = conversation_service.is_session_active(session_id)
    session_info = conversation_service.get_session_info(session_id)
    
    if not session_info:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'session_id': session_id,
        'is_active': is_active,
        'session_info': session_info
    }), 200

@app.route('/api/session/questions/<session_id>', methods=['GET'])
def get_session_questions(session_id):
    """Get all questions in the session"""
    questions = conversation_service.get_session_questions(session_id)
    
    return jsonify({
        'session_id': session_id,
        'questions': questions,
        'count': len(questions)
    }), 200

@app.route('/api/session/statistics', methods=['GET'])
def get_session_statistics():
    """Get session statistics"""
    stats = conversation_service.get_session_statistics()
    return jsonify(stats), 200

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    role = data.get('role', 'employee').strip()
    
    if not username or not email or not password:
        return jsonify({'error': 'Username, email and password are required'}), 400
    
    if role not in ['admin', 'employee']:
        return jsonify({'error': 'Role must be admin or employee'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    try:
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    # 添加调试日志
    logger.info(f"Login attempt for username: {username}")
    logger.info(f"Request origin: {request.headers.get('Origin')}")
    logger.info(f"Request referer: {request.headers.get('Referer')}")
    logger.info(f"Session before login: {dict(session)}")
    
    if not username or not password:
        logger.warning(f"Login failed: missing username or password")
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        # 设置session为永久性
        session.permanent = True
        
        logger.info(f"Login successful for user: {username}, role: {user.role}")
        logger.info(f"Session after login: {dict(session)}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    else:
        logger.warning(f"Login failed: invalid credentials for username: {username}")
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/current-user', methods=['GET'])
def current_user():
    # 添加调试日志
    logger.info(f"Current user check - Session: {dict(session)}")
    logger.info(f"Request origin: {request.headers.get('Origin')}")
    logger.info(f"Request referer: {request.headers.get('Referer')}")
    logger.info(f"Request cookies: {dict(request.cookies)}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    # 检查是否有认证信息
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            logger.info(f"Current user found: {user.username}, role: {user.role}")
            return jsonify(user.to_dict()), 200
        else:
            logger.warning(f"User ID in session but user not found in database: {session['user_id']}")
            # 清除无效的session
            session.clear()
            return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 401
    
    # 检查Authorization header作为备选方案
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        # 这里可以添加JWT token验证逻辑
        logger.info("Authorization header found, but JWT not implemented yet")
    
    logger.info("No user authenticated")
    return jsonify({
        'error': 'Not authenticated', 
        'code': 'NOT_AUTHENTICATED',
        'message': 'Please log in to access this resource'
    }), 401

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        db.session.commit()
        
        # Get database info for Azure monitoring
        db_info = db.session.execute(text("SELECT version()")).scalar()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'database_type': 'postgresql',
            'database_version': db_info.split()[1] if db_info else 'unknown',
            'timestamp': datetime.utcnow().isoformat(),
            'environment': app.config.get('FLASK_ENV', 'unknown'),
            'azure_deployment': app.config.get('AZURE_DEPLOYMENT', False)
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
            'environment': app.config.get('FLASK_ENV', 'unknown'),
            'azure_deployment': app.config.get('AZURE_DEPLOYMENT', False)
        }), 503

if __name__ == '__main__':
    # For production deployment, use proper WSGI server
    # Azure App Service will set PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if app.config.get('AZURE_APP_SERVICE') else '127.0.0.1'
    
    logger.info(f"Starting Flask app on {host}:{port}")
    logger.info(f"Environment: {app.config.get('FLASK_ENV', 'unknown')}")
    logger.info(f"Azure deployment: {app.config.get('AZURE_DEPLOYMENT', False)}")
    
    app.run(debug=app.config.get('DEBUG', False), host=host, port=port)