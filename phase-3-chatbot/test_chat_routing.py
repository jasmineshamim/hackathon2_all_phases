"""
Test all chat command routing rules.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def login_user():
    """Login and get token."""
    print("Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "testuser_1770600946@example.com",
            "password": "TestPass123!"
        }
    )
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Logged in as {data['email']}")
        return data['access_token'], data['user_id']
    else:
        print(f"[FAIL] Login failed: {response.text}")
        return None, None

def test_chat_command(token, user_id, message, test_name):
    """Send a chat message and display response."""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")
    print(f"User: {message}")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        json={"message": message},
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        # Remove Unicode for Windows console
        response_text = data.get('response', '').encode('ascii', 'ignore').decode('ascii')
        print(f"AI: {response_text}")
        print(f"Tool Calls: {len(data.get('tool_calls', []))}")
        if data.get('tool_calls'):
            for tc in data['tool_calls']:
                print(f"  - {tc.get('tool')}: {tc.get('parameters')}")
        return True
    else:
        print(f"[FAIL] {response.status_code}: {response.text}")
        return False

def main():
    print("="*70)
    print("CHAT COMMAND ROUTING TEST")
    print("="*70)

    # Login
    token, user_id = login_user()
    if not token:
        return

    # Test 1: Create task (Rule 1)
    test_chat_command(
        token, user_id,
        "Create a task to buy groceries",
        "Rule 1: Create Task"
    )

    time.sleep(1)

    # Test 2: Create another task with different phrasing
    test_chat_command(
        token, user_id,
        "Add a task for gym workout",
        "Rule 1: Create Task (variant)"
    )

    time.sleep(1)

    # Test 3: Create third task
    test_chat_command(
        token, user_id,
        "I need to remember to call dentist",
        "Rule 1: Create Task (variant 2)"
    )

    time.sleep(1)

    # Test 4: List all tasks (Rule 2)
    test_chat_command(
        token, user_id,
        "Show me my tasks",
        "Rule 2: List All Tasks"
    )

    time.sleep(1)

    # Test 5: List tasks with different phrasing
    test_chat_command(
        token, user_id,
        "What's on my todo list?",
        "Rule 2: List All Tasks (variant)"
    )

    time.sleep(1)

    # Test 6: Complete a task (Rule 5)
    test_chat_command(
        token, user_id,
        "Mark task 1 as complete",
        "Rule 5: Complete Task"
    )

    time.sleep(1)

    # Test 7: List completed tasks (Rule 3)
    test_chat_command(
        token, user_id,
        "Show me completed tasks",
        "Rule 3: List Completed Tasks"
    )

    time.sleep(1)

    # Test 8: List pending tasks (Rule 4)
    test_chat_command(
        token, user_id,
        "What tasks are still pending?",
        "Rule 4: List Pending Tasks"
    )

    time.sleep(1)

    # Test 9: Update a task (Rule 7)
    test_chat_command(
        token, user_id,
        "Update task 2 to 'Go to gym at 6pm'",
        "Rule 7: Update Task"
    )

    time.sleep(1)

    # Test 10: Delete a task (Rule 6)
    test_chat_command(
        token, user_id,
        "Delete task 3",
        "Rule 6: Delete Task"
    )

    time.sleep(1)

    # Test 11: List all tasks again to verify changes
    test_chat_command(
        token, user_id,
        "Show all my tasks",
        "Final: Verify All Changes"
    )

    print("\n" + "="*70)
    print("CHAT COMMAND ROUTING TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
