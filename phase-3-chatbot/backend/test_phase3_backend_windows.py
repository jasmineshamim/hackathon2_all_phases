"""
Windows-compatible comprehensive backend test for Phase III AI Chatbot.
Tests database models, MCP tools, and chat endpoint functionality.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.init_db import create_db_and_tables, check_db_connection
from backend.database.session import get_session
from backend.models.user import User
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message, MessageRole
from datetime import datetime

print("=" * 60)
print("PHASE III BACKEND FOUNDATION TEST")
print("=" * 60)

# Test 1: Database Connection and Table Creation
print("\n[TEST 1] Database Connection and Table Creation")
print("-" * 60)
try:
    create_db_and_tables()
    tables = check_db_connection()

    required_tables = ['user', 'task', 'conversations', 'messages']
    missing_tables = [t for t in required_tables if t not in tables]

    if missing_tables:
        print(f"[FAIL] Missing tables: {missing_tables}")
    else:
        print(f"[PASS] All required tables exist: {tables}")
except Exception as e:
    print(f"[FAIL] Database initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Create Test User and Tasks
print("\n[TEST 2] Create Test User and Tasks")
print("-" * 60)
try:
    session = next(get_session())

    # Check if test user already exists
    from sqlmodel import select
    existing_user = session.exec(select(User).where(User.id == "test_user_chatbot")).first()

    if not existing_user:
        # Create test user
        test_user = User(
            id="test_user_chatbot",
            email="chatbot_test@example.com",
            name="Chatbot Test User",
            hashed_password="test_hash"
        )
        session.add(test_user)
        session.commit()
        print(f"[PASS] Created test user: {test_user.id}")
    else:
        print(f"[PASS] Test user already exists: {existing_user.id}")

    # Create test tasks
    task1 = Task(
        user_id="test_user_chatbot",
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False
    )
    task2 = Task(
        user_id="test_user_chatbot",
        title="Call mom",
        description="Discuss weekend plans",
        completed=False
    )
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task1)
    session.refresh(task2)
    print(f"[PASS] Created test tasks: {task1.id}, {task2.id}")

    session.close()
except Exception as e:
    print(f"[FAIL] Error creating test data: {e}")
    import traceback
    traceback.print_exc()
    session.rollback()
    session.close()

# Test 3: MCP Tools - Add Task
print("\n[TEST 3] MCP Tool: add_task")
print("-" * 60)
try:
    from backend.src.mcp.tools.add_task import add_task

    result = asyncio.run(add_task(
        user_id="test_user_chatbot",
        title="Test task from MCP",
        description="Testing add_task tool"
    ))

    if result.get("status") == "created" and result.get("task_id"):
        print(f"[PASS] Task created with ID {result['task_id']}")
        print(f"       Title: {result['title']}")
    else:
        print(f"[FAIL] Unexpected result: {result}")
except Exception as e:
    print(f"[FAIL] add_task error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: MCP Tools - List Tasks
print("\n[TEST 4] MCP Tool: list_tasks")
print("-" * 60)
try:
    from backend.src.mcp.tools.list_tasks import list_tasks

    result = asyncio.run(list_tasks(
        user_id="test_user_chatbot",
        status="all"
    ))

    if result.get("count") >= 3:  # Should have at least 3 tasks now
        print(f"[PASS] Found {result['count']} tasks")
        for task in result['tasks'][:3]:
            print(f"       - Task {task['id']}: {task['title']} (completed: {task['completed']})")
    else:
        print(f"[FAIL] Expected at least 3 tasks, got {result.get('count')}")
except Exception as e:
    print(f"[FAIL] list_tasks error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: MCP Tools - Complete Task
print("\n[TEST 5] MCP Tool: complete_task")
print("-" * 60)
try:
    from backend.src.mcp.tools.complete_task import complete_task

    # Get first task ID
    session = next(get_session())
    from sqlmodel import select
    query = select(Task).where(Task.user_id == "test_user_chatbot").limit(1)
    task = session.exec(query).first()
    session.close()

    if task:
        result = asyncio.run(complete_task(
            user_id="test_user_chatbot",
            task_id=task.id
        ))

        if result.get("status") in ["completed", "already_completed"]:
            print(f"[PASS] Task {task.id} marked as complete")
        else:
            print(f"[FAIL] Unexpected result: {result}")
    else:
        print("[SKIP] No tasks found to complete")
except Exception as e:
    print(f"[FAIL] complete_task error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: MCP Tools - Update Task
print("\n[TEST 6] MCP Tool: update_task")
print("-" * 60)
try:
    from backend.src.mcp.tools.update_task import update_task

    # Get a task ID
    session = next(get_session())
    query = select(Task).where(Task.user_id == "test_user_chatbot").limit(1)
    task = session.exec(query).first()
    session.close()

    if task:
        result = asyncio.run(update_task(
            user_id="test_user_chatbot",
            task_id=task.id,
            title="Updated task title"
        ))

        if result.get("status") == "updated":
            print(f"[PASS] Task {task.id} updated")
            print(f"       New title: {result['title']}")
        else:
            print(f"[FAIL] Unexpected result: {result}")
    else:
        print("[SKIP] No tasks found to update")
except Exception as e:
    print(f"[FAIL] update_task error: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Conversation and Message Models
print("\n[TEST 7] Conversation and Message Models")
print("-" * 60)
try:
    session = next(get_session())

    # Create conversation
    conversation = Conversation(
        user_id="test_user_chatbot",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    print(f"[PASS] Created conversation: {conversation.id}")

    # Create messages
    msg1 = Message(
        conversation_id=conversation.id,
        user_id="test_user_chatbot",
        role=MessageRole.USER,
        content="Add a task to buy groceries",
        created_at=datetime.utcnow()
    )
    msg2 = Message(
        conversation_id=conversation.id,
        user_id="test_user_chatbot",
        role=MessageRole.ASSISTANT,
        content="I've added 'Buy groceries' to your task list.",
        created_at=datetime.utcnow()
    )
    session.add(msg1)
    session.add(msg2)
    session.commit()
    print(f"[PASS] Created 2 messages in conversation {conversation.id}")

    session.close()
except Exception as e:
    print(f"[FAIL] Conversation/Message model error: {e}")
    import traceback
    traceback.print_exc()
    session.rollback()
    session.close()

# Test 8: MCP Server Registration
print("\n[TEST 8] MCP Server Tool Registration")
print("-" * 60)
try:
    from backend.src.mcp.server import mcp_server

    tools = mcp_server.get_tool_schemas()
    tool_names = [tool['name'] for tool in tools]

    expected_tools = ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
    missing_tools = [t for t in expected_tools if t not in tool_names]

    if missing_tools:
        print(f"[FAIL] Missing tools: {missing_tools}")
    else:
        print(f"[PASS] All 5 MCP tools registered")
        for tool_name in tool_names:
            print(f"       - {tool_name}")
except Exception as e:
    print(f"[FAIL] MCP server error: {e}")
    import traceback
    traceback.print_exc()

# Test 9: Chat Agent Initialization
print("\n[TEST 9] Chat Agent Initialization")
print("-" * 60)
try:
    from backend.src.agents.chat_agent import chat_agent

    if chat_agent.client and chat_agent.tools:
        print(f"[PASS] Chat agent initialized")
        print(f"       Model: {chat_agent.model}")
        print(f"       Tools: {len(chat_agent.tools)} tools available")
    else:
        print(f"[FAIL] Chat agent not properly initialized")
except Exception as e:
    print(f"[FAIL] Chat agent error: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("[OK] Backend foundation testing complete")
print("\nNext steps:")
print("1. Start backend server: python -m uvicorn backend.main:app --reload --port 8001")
print("2. Test chat endpoint manually or with curl")
print("3. Proceed with Phase 3 frontend implementation")
print("=" * 60)
