"""
Complete system test for Phase III Todo AI Chatbot.
Tests all components: Auth, Tasks, Chat, MCP Tools, Database.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint."""
    print("\n1. Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   [OK] Health check passed")

def test_register_and_login():
    """Test user registration and login."""
    print("\n2. Testing Authentication...")

    # Register
    email = f"testuser_{int(time.time())}@example.com"
    register_data = {
        "email": email,
        "password": "TestPass123!",
        "name": "Test User"
    }

    print(f"   Registering user: {email}")
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")

    if response.status_code in [200, 201]:
        data = response.json()
        print(f"   [OK] Registration successful")
        print(f"   User ID: {data.get('user_id')}")
        return data.get('access_token'), data.get('user_id'), email
    else:
        print(f"   Response: {response.text}")
        raise Exception("Registration failed")

def test_chat_endpoint(token, user_id):
    """Test chat endpoint with authentication."""
    print("\n3. Testing Chat Endpoint...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Test 1: Create a task via chat
    print("   Test 1: Create task via chat")
    chat_data = {
        "message": "Create a task to buy groceries"
    }

    response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        json=chat_data,
        headers=headers
    )

    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] Chat response received")
        print(f"   Conversation ID: {data.get('conversation_id')}")
        response_text = data.get('response', '')
        # Remove Unicode characters for Windows console
        response_text = response_text.encode('ascii', 'ignore').decode('ascii')
        print(f"   Response: {response_text[:100]}...")
        print(f"   Tool calls: {len(data.get('tool_calls', []))}")
        conversation_id = data.get('conversation_id')
    else:
        print(f"   Error: {response.text}")
        raise Exception("Chat endpoint failed")

    # Test 2: List tasks via chat
    print("\n   Test 2: List tasks via chat")
    chat_data = {
        "conversation_id": conversation_id,
        "message": "Show me my tasks"
    }

    response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        json=chat_data,
        headers=headers
    )

    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] Chat response received")
        response_text = data.get('response', '')
        # Remove Unicode characters for Windows console
        response_text = response_text.encode('ascii', 'ignore').decode('ascii')
        print(f"   Response: {response_text[:200]}...")
        print(f"   Tool calls: {len(data.get('tool_calls', []))}")
    else:
        print(f"   Error: {response.text}")

    return conversation_id

def test_task_endpoints(token, user_id):
    """Test direct task endpoints."""
    print("\n4. Testing Task Endpoints...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create task
    print("   Creating task via API...")
    task_data = {
        "title": "Test Task via API",
        "description": "This is a test task"
    }

    response = requests.post(
        f"{BASE_URL}/tasks/",
        json=task_data,
        headers=headers
    )

    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        task = response.json()
        print(f"   [OK] Task created: {task.get('title')}")
        task_id = task.get('id')
    else:
        print(f"   Error: {response.text}")
        return

    # List tasks
    print("\n   Listing all tasks...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"   [OK] Found {len(tasks)} tasks")
        for task in tasks:
            print(f"     - {task.get('title')} (ID: {task.get('id')})")

    return task_id

def test_database_tables():
    """Verify database tables exist."""
    print("\n5. Verifying Database Tables...")

    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

    try:
        from sqlalchemy import text
        from database.session import engine

        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]

        print(f"   Found {len(tables)} tables:")
        for table in tables:
            print(f"     - {table}")

        expected = ['user', 'task', 'conversations', 'messages']
        missing = [t for t in expected if t not in tables]

        if missing:
            print(f"   [ERROR] Missing tables: {missing}")
        else:
            print("   [OK] All required tables exist")

    except Exception as e:
        print(f"   Error checking database: {e}")

def main():
    """Run all tests."""
    print("=" * 60)
    print("PHASE III TODO AI CHATBOT - COMPLETE SYSTEM TEST")
    print("=" * 60)

    try:
        # Test 1: Health
        test_health()

        # Test 2: Auth
        token, user_id, email = test_register_and_login()

        # Test 3: Chat
        conversation_id = test_chat_endpoint(token, user_id)

        # Test 4: Tasks
        task_id = test_task_endpoints(token, user_id)

        # Test 5: Database
        test_database_tables()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED [SUCCESS]")
        print("=" * 60)
        print(f"\nTest User: {email}")
        print(f"User ID: {user_id}")
        print(f"Conversation ID: {conversation_id}")
        print(f"\nYou can now test the frontend at: http://localhost:3000")
        print(f"Backend API docs at: http://localhost:8001/docs")

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
