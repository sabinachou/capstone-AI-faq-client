#!/usr/bin/env python3
"""
Detailed AI Service Diagnosis for Azure Production
"""

import requests
import json

def test_azure_ai_detailed():
    """Detailed test of AI service in Azure production"""
    print("🔍 Detailed AI Service Diagnosis for Azure Production")
    print("=" * 60)
    
    # Test 1: Check if we can get more detailed error info
    print("\n1️⃣ Testing AI service with detailed error logging...")
    try:
        # Login first
        session = requests.Session()
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        login_response = session.post(
            "https://faq-ai-system-backend.azurewebsites.net/api/login",
            json=login_data,
            headers={'Origin': 'https://purple-bay-044a4fe1e-preview.westus2.1.azurestaticapps.net'}
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Test with different types of questions to see if it's a specific issue
            test_questions = [
                "What is AI?",
                "How to reset password?",
                "What are the company policies?",
                "Tell me about the FAQ system"
            ]
            
            for i, question in enumerate(test_questions, 1):
                print(f"\n🔄 Test {i}: {question}")
                chat_data = {"question": question}
                
                chat_response = session.post(
                    "https://faq-ai-system-backend.azurewebsites.net/api/chat",
                    json=chat_data,
                    headers={'Origin': 'https://purple-bay-044a4fe1e-preview.westus2.1.azurestaticapps.net'}
                )
                
                if chat_response.status_code == 200:
                    data = chat_response.json()
                    answer = data.get('answer', 'No answer')
                    source = data.get('source', 'Unknown')
                    confidence = data.get('confidence', 'Unknown')
                    
                    print(f"   Status: 200")
                    print(f"   Source: {source}")
                    print(f"   Confidence: {confidence}")
                    print(f"   Answer: {answer[:100]}...")
                    
                    # Check if it's the error message
                    if "temporarily unavailable" in answer:
                        print("   ❌ AI service error detected")
                    else:
                        print("   ✅ AI service working")
                else:
                    print(f"   Status: {chat_response.status_code}")
                    print(f"   Error: {chat_response.text}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Detailed test failed: {e}")
        import traceback
        traceback.print_exc()

def test_azure_environment():
    """Test Azure environment configuration"""
    print("\n2️⃣ Testing Azure environment configuration...")
    try:
        # Check if we can access the backend directly
        response = requests.get("https://faq-ai-system-backend.azurewebsites.net/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend environment: {data.get('environment', 'Unknown')}")
            print(f"✅ Azure deployment: {data.get('azure_deployment', 'Unknown')}")
            print(f"✅ Database: {data.get('database', 'Unknown')}")
            
            # Check if there are any specific Azure-related configurations
            print(f"✅ Backend status: {data.get('status', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Environment check failed: {e}")

def test_network_connectivity():
    """Test network connectivity from local to Azure and external services"""
    print("\n3️⃣ Testing network connectivity...")
    
    # Test 1: Local to Azure
    print("🔄 Testing local to Azure connectivity...")
    try:
        response = requests.get("https://faq-ai-system-backend.azurewebsites.net/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Local to Azure: Connected")
        else:
            print(f"❌ Local to Azure: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Local to Azure: {e}")
    
    # Test 2: Local to OpenAI API
    print("🔄 Testing local to OpenAI API connectivity...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex(('api.chatanywhere.org', 443))
        sock.close()
        
        if result == 0:
            print("✅ Local to OpenAI API: Connected")
        else:
            print(f"❌ Local to OpenAI API: Connection failed (error code: {result})")
    except Exception as e:
        print(f"❌ Local to OpenAI API: {e}")
    
    # Test 3: Azure to OpenAI API (this would need to be run on Azure)
    print("🔄 Testing Azure to OpenAI API connectivity...")
    print("   ℹ️ This test needs to be run on Azure to check actual connectivity")
    print("   💡 You can check this in Azure App Service logs or by running a test on Azure")

def suggest_solutions():
    """Suggest solutions based on the diagnosis"""
    print("\n4️⃣ Suggested Solutions...")
    print("=" * 40)
    
    print("🔍 Based on the diagnosis, here are the most likely issues:")
    print()
    
    print("1️⃣ **Azure Environment Variable Issue**")
    print("   - Check if OPENAI_API_KEY is correctly set in Azure App Service")
    print("   - Verify the environment variable name and value")
    print("   - Restart the App Service after changing environment variables")
    print()
    
    print("2️⃣ **Azure Network Restrictions**")
    print("   - Azure App Service might have outbound network restrictions")
    print("   - Check if api.chatanywhere.org is accessible from Azure")
    print("   - Consider using Azure OpenAI service instead")
    print()
    
    print("3️⃣ **Code Deployment Issue**")
    print("   - Ensure the latest code with AI service fixes is deployed")
    print("   - Check Azure deployment logs for any errors")
    print("   - Verify the deployment was successful")
    print()
    
    print("4️⃣ **Azure App Service Configuration**")
    print("   - Check if the App Service plan supports external API calls")
    print("   - Verify there are no firewall or security group restrictions")
    print("   - Check App Service logs for specific error messages")

if __name__ == "__main__":
    test_azure_ai_detailed()
    test_azure_environment()
    test_network_connectivity()
    suggest_solutions()
    print("\n🎉 Detailed diagnosis completed!")

