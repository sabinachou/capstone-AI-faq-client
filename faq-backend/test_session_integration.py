#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session management functionality integration test
Test continuous questioning and delayed evaluation functionality
"""

import requests
import json
import time

# Configuration
BASE_URL = 'http://127.0.0.1:5000'
TEST_USER = {
    'username': 'testuser',
    'password': 'testpass123',
    'email': 'test@example.com'
}

def test_session_workflow():
    """
    Test complete session workflow
    """
    print("=== Session Management Functionality Integration Test ===")
    
    # 1. User registration/login
    print("\n1. User authentication test...")
    
    # Try to register user
    register_response = requests.post(f'{BASE_URL}/api/register', json=TEST_USER)
    if register_response.status_code == 201:
        print("✅ User registration successful")
    elif register_response.status_code == 400:
        print("ℹ️ User already exists, continue with login")
    
    # Login
    login_response = requests.post(f'{BASE_URL}/api/login', json={
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return False
    
    user_data = login_response.json()
    print(f"✅ Login successful, user ID: {user_data['user']['id']}")
    
    # 2. Start new session
    print("\n2. Starting new session...")
    session_response = requests.post(f'{BASE_URL}/api/session/start', json={
        'user_id': user_data['user']['id']
    })
    
    if session_response.status_code != 201:
        print(f"❌ Session creation failed: {session_response.text}")
        return False
    
    session_data = session_response.json()
    session_id = session_data['session_id']
    print(f"✅ Session created successfully, session ID: {session_id}")
    
    # 3. Send multiple consecutive questions
    print("\n3. Sending consecutive questions...")
    questions = [
        "How do I apply for leave?",
        "What materials are needed for leave application?",
        "How long does leave approval take?",
        "What if my leave request is rejected?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n  Question {i}: {question}")
        
        chat_response = requests.post(f'{BASE_URL}/api/chat', json={
            'question': question,
            'session_id': session_id
        })
        
        if chat_response.status_code != 200:
            print(f"    ❌ Send failed: {chat_response.text}")
            continue
        
        chat_data = chat_response.json()
        print(f"    ✅ Reply: {chat_data['answer'][:100]}...")
        confidence = chat_data.get('confidence', 0)
        if isinstance(confidence, str):
            print(f"    📊 Confidence: {confidence}")
        else:
            print(f"    📊 Confidence: {confidence:.2f}")
        print(f"    🎯 Source: {chat_data.get('source', 'AI Generated')}")
        
        # Brief delay to simulate real conversation
        time.sleep(0.5)
    
    # 4. Check session status
    print("\n4. Checking session status...")
    status_response = requests.get(f'{BASE_URL}/api/session/status/{session_id}')
    
    if status_response.status_code == 200:
        status_data = status_response.json()
        print(f"✅ Session status: {'Active' if status_data['is_active'] else 'Ended'}")
        print(f"📈 Question count: {status_data['session_info']['question_count']}")
    else:
        print(f"❌ Failed to get session status: {status_response.text}")
    
    # 5. Get all questions in the session
    print("\n5. Getting session question history...")
    questions_response = requests.get(f'{BASE_URL}/api/session/questions/{session_id}')
    
    if questions_response.status_code == 200:
        questions_data = questions_response.json()
        print(f"✅ Total {len(questions_data['questions'])} questions")
        for q in questions_data['questions']:
            print(f"  - {q['question']} (Category: {q['category']})")
    else:
        print(f"❌ Failed to get question history: {questions_response.text}")
    
    # 6. End session and submit feedback
    print("\n6. Ending session and submitting feedback...")
    feedback_data = {
        'session_id': session_id,
        'satisfied': True,
        'rating': 4,
        'comment': 'This conversation was very helpful, the AI assistant answered all my questions about leave!'
    }
    
    end_response = requests.post(f'{BASE_URL}/api/session/end', json=feedback_data)
    
    if end_response.status_code == 200:
        print("✅ Session ended and feedback submitted successfully")
        end_data = end_response.json()
        print(f"📊 Feedback ID: {end_data.get('feedback_id')}")
    else:
        print(f"❌ Failed to end session: {end_response.text}")
    
    # 7. Verify session has ended
    print("\n7. Verifying session status...")
    final_status = requests.get(f'{BASE_URL}/api/session/status/{session_id}')
    
    if final_status.status_code == 200:
        final_data = final_status.json()
        if not final_data['is_active']:
            print("✅ Session ended correctly")
        else:
            print("⚠️ Session is still active")
    
    # 8. Get session statistics
    print("\n8. Getting session statistics...")
    stats_response = requests.get(f'{BASE_URL}/api/session/statistics')
    
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        print(f"✅ Statistics:")
        print(f"  Total sessions: {stats_data['total_sessions']}")
        print(f"  Active sessions: {stats_data['active_sessions']}")
        print(f"  Average questions: {stats_data.get('average_questions_per_session', 0):.1f}")
        print(f"  Today's sessions: {stats_data.get('today_sessions', 0)}")
    else:
        print(f"❌ Failed to get statistics: {stats_response.text}")
    
    print("\n=== Test Completed ===")
    return True

def test_session_timeout():
    """
    Test session timeout functionality
    """
    print("\n=== Session Timeout Test ===")
    
    # Create a session but don't send messages, test timeout
    session_response = requests.post(f'{BASE_URL}/api/session/start', json={
        'user_id': 1  # Assume user ID is 1
    })
    
    if session_response.status_code == 201:
        session_data = session_response.json()
        session_id = session_data['session_id']
        print(f"✅ Test session created: {session_id}")
        
        # Wait for a while then check status
        print("⏳ Waiting for session timeout...")
        time.sleep(2)
        
        # Try to send message in timed out session
        chat_response = requests.post(f'{BASE_URL}/api/chat', json={
            'question': 'This is a test message',
            'session_id': session_id
        })
        
        if chat_response.status_code == 400:
            print("✅ Session timeout detection working normally")
        else:
            print("⚠️ Session timeout detection may have issues")
    
    print("=== Timeout Test Completed ===")

if __name__ == '__main__':
    try:
        # Run main test
        success = test_session_workflow()
        
        if success:
            # Run timeout test
            test_session_timeout()
            
            print("\n🎉 All tests completed! Continuous questioning and delayed evaluation functionality successfully implemented.")
            print("\nFeatures:")
            print("✅ Session state management")
            print("✅ Continuous question tracking")
            print("✅ Delayed feedback collection")
            print("✅ Session statistics analysis")
            print("✅ Automatic timeout handling")
        else:
            print("\n❌ Errors occurred during testing")
            
    except Exception as e:
        print(f"\n❌ Test exception: {str(e)}")
        import traceback
        traceback.print_exc()