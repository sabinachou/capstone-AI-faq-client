#!/usr/bin/env python3
"""
Comprehensive AI Service Diagnosis Script
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment configuration"""
    print("🔍 Environment Configuration Test")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OpenAI API Key: {api_key[:20]}...")
        print(f"   Length: {len(api_key)} characters")
        print(f"   Format: {'Valid' if api_key.startswith('sk-') else 'Invalid'}")
    else:
        print("❌ OpenAI API Key not found")
        return False
    
    # Check Python packages
    try:
        import openai
        print(f"✅ OpenAI library: {openai.__version__}")
    except ImportError as e:
        print(f"❌ OpenAI library not installed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy not installed: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn: {sklearn.__version__}")
    except ImportError as e:
        print(f"❌ Scikit-learn not installed: {e}")
        return False
    
    return True

def test_ai_service_import():
    """Test AI service module import"""
    print("\n📦 AI Service Module Test")
    print("=" * 50)
    
    try:
        from ai_service import AIService
        print("✅ AI Service module imported successfully")
        return True
    except Exception as e:
        print(f"❌ AI Service import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_service_instance():
    """Test AI service instance creation"""
    print("\n🏗️ AI Service Instance Test")
    print("=" * 50)
    
    try:
        from ai_service import AIService
        ai_service = AIService()
        print("✅ AI Service instance created successfully")
        
        # Check API key in instance
        if ai_service.openai_api_key:
            print(f"✅ API Key in instance: {ai_service.openai_api_key[:20]}...")
        else:
            print("❌ No API key in instance")
            return False
        
        return ai_service
    except Exception as e:
        print(f"❌ AI Service instance creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_openai_connection(ai_service):
    """Test OpenAI API connection"""
    print("\n🌐 OpenAI API Connection Test")
    print("=" * 50)
    
    try:
        # Test direct OpenAI client creation
        import openai
        client = openai.OpenAI(
            api_key=ai_service.openai_api_key,
            base_url="https://api.chatanywhere.org/v1"
        )
        print("✅ OpenAI client created successfully")
        
        # Test API call
        print("🔄 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, test message"}],
            max_tokens=10
        )
        
        print("✅ API call successful!")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_service_methods(ai_service):
    """Test AI service methods"""
    print("\n🔧 AI Service Methods Test")
    print("=" * 50)
    
    try:
        # Test generate_ai_response method
        print("🔄 Testing generate_ai_response method...")
        response = ai_service.generate_ai_response("What is artificial intelligence?")
        print("✅ generate_ai_response method successful!")
        print(f"   Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ AI service method test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main diagnosis function"""
    print("🚀 AI Service Comprehensive Diagnosis")
    print("=" * 60)
    
    # Test 1: Environment
    if not test_environment():
        print("\n❌ Environment test failed. Please check your configuration.")
        return
    
    # Test 2: Module import
    if not test_ai_service_import():
        print("\n❌ Module import test failed. Please check your code.")
        return
    
    # Test 3: Instance creation
    ai_service = test_ai_service_instance()
    if not ai_service:
        print("\n❌ Instance creation test failed. Please check your code.")
        return
    
    # Test 4: OpenAI connection
    if not test_openai_connection(ai_service):
        print("\n❌ OpenAI connection test failed. Please check your API key and network.")
        return
    
    # Test 5: AI service methods
    if not test_ai_service_methods(ai_service):
        print("\n❌ AI service methods test failed. Please check your implementation.")
        return
    
    print("\n🎉 All tests passed! AI service should be working correctly.")
    print("\n💡 If you're still experiencing issues, check:")
    print("   1. Network connectivity to api.chatanywhere.org")
    print("   2. API key validity and quota")
    print("   3. Backend logs for specific error messages")

if __name__ == "__main__":
    main()
