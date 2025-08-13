
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///faq.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # AI Service Configuration
    AI_SIMILARITY_THRESHOLD = float(os.environ.get('AI_SIMILARITY_THRESHOLD', '0.3'))
    AI_MAX_TOKENS = int(os.environ.get('AI_MAX_TOKENS', '500'))
    AI_TEMPERATURE = float(os.environ.get('AI_TEMPERATURE', '0.7'))