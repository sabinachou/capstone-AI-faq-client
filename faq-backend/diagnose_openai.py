#!/usr/bin/env python3
"""
OpenAI Function Diagnostic Script
Used to check OpenAI API configuration and connection issues
"""

import os
import sys
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check environment configuration"""
    print("🔍 Environment Configuration Check")
    print("=" * 50)
    
    # Check .env file
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✅ .env file exists")
    else:
        print("❌ .env file does not exist")
        print("   Recommend creating .env file to store API key")
    
    # Check environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY environment variable is set")
        print(f"   Key first 20 characters: {api_key[:20]}...")
    else:
        print("❌ OPENAI_API_KEY environment variable is not set")
    
    # Check Python packages
    try:
        import openai
        print(f"✅ OpenAI library is installed, version: {openai.__version__}")
    except ImportError:
        print("❌ OpenAI library is not installed")
        return False
    
    return True

def test_api_key():
    """Test API key"""
    print("\n🔑 API Key Test")
    print("=" * 50)
    
    # Get key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        print("   Please set OPENAI_API_KEY in .env file")
        return False
    
    # Test key format
    if not api_key.startswith('sk-'):
        print("❌ API key format is incorrect")
        print("   Key should start with 'sk-'")
        return False
    
    print(f"✅ API key format is correct: {api_key[:20]}...")
    
    # Test API call
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ API call successful")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except openai.AuthenticationError:
        print("❌ Authentication failed - API key is invalid")
        return False
    except openai.RateLimitError:
        print("❌ Rate limit exceeded - Please try again later")
        return False
    except openai.QuotaExceededError:
        print("❌ Quota exceeded - Please check account balance")
        return False
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False

def test_config_integration():
    """Test configuration integration"""
    print("\n⚙️ Configuration Integration Test")
    print("=" * 50)
    
    try:
        from config import Config
        print("✅ Configuration module imported successfully")
        
        if Config.OPENAI_API_KEY:
            print(f"✅ API key in configuration: {Config.OPENAI_API_KEY[:20]}...")
        else:
            print("❌ No API key in configuration")
            
    except Exception as e:
        print(f"❌ Configuration module import failed: {e}")
        return False
    
    return True

def test_ai_service():
    """Test AI service"""
    print("\n🤖 AI Service Test")
    print("=" * 50)
    
    try:
        from ai_service import AIService
        print("✅ AI service module imported successfully")
        
        ai_service = AIService()
        print("✅ AI service instance created successfully")
        
        if ai_service.openai_api_key:
            print(f"✅ API key in AI service: {ai_service.openai_api_key[:20]}...")
        else:
            print("❌ No API key in AI service")
            
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 OpenAI Function Diagnostic Tool")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed, please resolve environment issues first")
        return
    
    # Test API key
    api_ok = test_api_key()
    
    # Test configuration integration
    config_ok = test_config_integration()
    
    # Test AI service
    service_ok = test_ai_service()
    
    # Summary
    print("\n📊 Diagnostic Results Summary")
    print("=" * 60)
    
    if api_ok and config_ok and service_ok:
        print("🎉 All checks passed! OpenAI functionality should work normally.")
    else:
        print("⚠️ Some issues were found that need to be resolved:")
        
        if not api_ok:
            print("   - API key configuration issue")
        if not config_ok:
            print("   - Configuration module issue")
        if not service_ok:
            print("   - AI service module issue")
        
        print("\n💡 Resolution suggestions:")
        print("   1. Check OPENAI_API_KEY setting in .env file")
        print("   2. Confirm API key is valid and has balance")
        print("   3. Check network connection")
        print("   4. View application logs for detailed error information")

if __name__ == "__main__":
    main()
