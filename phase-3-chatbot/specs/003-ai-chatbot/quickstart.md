# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08
**Phase**: Phase 1 - Setup & Testing

## Overview

This guide provides step-by-step instructions for setting up and testing the AI chatbot feature locally. Follow these instructions to get the conversational task management interface running on your development machine.

## Prerequisites

### Required Software
- **Node.js**: v18+ (for Next.js frontend)
- **Python**: 3.11+ (for FastAPI backend)
- **PostgreSQL**: Access to Neon Serverless PostgreSQL database
- **Git**: For version control
- **OpenAI API Key**: Required for AI agent functionality

### Required Accounts
- **OpenAI Account**: For API access and ChatKit domain configuration
- **Neon Account**: For PostgreSQL database (free tier available)
- **Better Auth**: Already configured from Phase II

---

## Setup Instructions

### Step 1: Environment Configuration

#### Backend Environment Variables

Create `backend/.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# OpenAI
OPENAI_API_KEY=sk-...your-openai-api-key...

# Authentication (from Phase II)
BETTER_AUTH_SECRET=your-better-auth-secret

# Server
PORT=8000
HOST=0.0.0.0
```

#### Frontend Environment Variables

Create `frontend/.env.local` file:

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# OpenAI ChatKit
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here

# Authentication (from Phase II)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

---

### Step 2: Database Setup

#### Run Database Migrations

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run Alembic migrations
alembic upgrade head

# Verify tables were created
psql $DATABASE_URL -c "\dt"
# Should show: users, tasks, conversations, messages
```

#### Verify Database Schema

```bash
# Check conversations table
psql $DATABASE_URL -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'conversations';"

# Check messages table
psql $DATABASE_URL -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'messages';"

# Verify indexes
psql $DATABASE_URL -c "SELECT indexname, tablename FROM pg_indexes WHERE tablename IN ('conversations', 'messages');"
```

---

### Step 3: Backend Setup

#### Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Verify MCP Server

```bash
# Test MCP tool imports
python -c "from src.mcp.server import mcp_server; print('MCP server loaded successfully')"

# List available tools
python -c "from src.mcp.server import mcp_server; print([tool.name for tool in mcp_server.tools])"
# Expected output: ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
```

#### Start Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Server should start at http://localhost:8000
# Check health: curl http://localhost:8000/health
```

---

### Step 4: Frontend Setup

#### Install Node Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Verify OpenAI ChatKit is installed
npm list @openai/chatkit
```

#### Configure OpenAI Domain Allowlist

**Important**: For production deployment, you must configure the domain allowlist.

1. Deploy frontend to get production URL (e.g., `https://your-app.vercel.app`)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Click "Add domain"
4. Enter your frontend URL (without trailing slash)
5. Save and copy the domain key
6. Add domain key to `frontend/.env.local`:
   ```
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here
   ```

**Note**: Local development (`localhost`) typically works without domain configuration.

#### Start Frontend Server

```bash
# Development mode
npm run dev

# Frontend should start at http://localhost:3000
```

---

## Testing the Chatbot

### Manual Testing Flow

#### 1. Authentication
```bash
# Open browser: http://localhost:3000
# Click "Sign In"
# Enter credentials (from Phase II setup)
# Should redirect to dashboard
```

#### 2. Access Chat Interface
```bash
# Navigate to: http://localhost:3000/chat
# Or click "Chat" link in navigation
# Should see OpenAI ChatKit interface
```

#### 3. Test Task Creation
```
User: "Add a task to buy groceries"
Expected Response: "I've added 'Buy groceries' to your task list."
Verify: Check database or dashboard for new task
```

#### 4. Test Task Listing
```
User: "Show me my tasks"
Expected Response: List of tasks with status
Verify: Response includes all user's tasks
```

#### 5. Test Task Completion
```
User: "Mark task 1 as complete"
Expected Response: "I've marked 'Buy groceries' as complete."
Verify: Task status updated in database
```

#### 6. Test Task Update
```
User: "Change task 1 to 'Buy groceries and fruits'"
Expected Response: "I've updated the task title."
Verify: Task title updated in database
```

#### 7. Test Task Deletion
```
User: "Delete task 1"
Expected Response: "I've deleted 'Buy groceries and fruits'."
Verify: Task removed from database
```

#### 8. Test Conversation Persistence
```
1. Send several messages
2. Close browser
3. Reopen and navigate to chat
Expected: Previous conversation history is displayed
```

---

## Automated Testing

### Backend Unit Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_mcp_tools.py

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Backend Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Test chat endpoint
pytest tests/integration/test_chat_endpoint.py -v

# Test conversation flow
pytest tests/integration/test_conversation_flow.py -v
```

### Frontend E2E Tests

```bash
cd frontend

# Run Cypress tests
npm run cypress:open

# Run headless
npm run cypress:run

# Run specific test
npm run cypress:run --spec "cypress/e2e/chat-flow.cy.ts"
```

---

## Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**:
```bash
# Verify environment variable is set
echo $OPENAI_API_KEY

# If empty, add to backend/.env:
OPENAI_API_KEY=sk-...your-key...

# Restart backend server
```

### Issue: "Database connection failed"

**Solution**:
```bash
# Test database connection
psql $DATABASE_URL -c "SELECT 1;"

# If fails, verify DATABASE_URL in backend/.env
# Check Neon dashboard for connection string
# Ensure IP is whitelisted in Neon settings
```

### Issue: "Conversation not persisting"

**Solution**:
```bash
# Check if messages table exists
psql $DATABASE_URL -c "\d messages"

# If not exists, run migrations
cd backend
alembic upgrade head

# Verify data is being stored
psql $DATABASE_URL -c "SELECT COUNT(*) FROM messages;"
```

### Issue: "ChatKit not loading"

**Solution**:
```bash
# Check if @openai/chatkit is installed
cd frontend
npm list @openai/chatkit

# If not installed:
npm install @openai/chatkit

# Verify NEXT_PUBLIC_OPENAI_DOMAIN_KEY is set
cat .env.local | grep OPENAI_DOMAIN_KEY

# For local development, domain key may not be required
```

### Issue: "JWT token invalid"

**Solution**:
```bash
# Verify BETTER_AUTH_SECRET matches between frontend and backend
# Frontend: .env.local
# Backend: .env

# Clear browser cookies and re-login
# Check token in browser DevTools > Application > Cookies
```

### Issue: "MCP tools not working"

**Solution**:
```bash
# Verify MCP server is initialized
cd backend
python -c "from src.mcp.server import mcp_server; print(mcp_server.tools)"

# Check tool function signatures
python -c "from src.mcp.tools.add_task import add_task; import inspect; print(inspect.signature(add_task))"

# Test tool directly
python -c "from src.mcp.tools.add_task import add_task; import asyncio; print(asyncio.run(add_task('user_123', 'Test task')))"
```

---

## Performance Testing

### Load Testing with Locust

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login and get JWT token
        response = self.client.post("/api/auth/signin", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["token"]

    @task
    def send_chat_message(self):
        self.client.post(
            "/api/user_123/chat",
            json={"message": "Show me my tasks"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000

# Open browser: http://localhost:8089
# Set users: 100, spawn rate: 10
# Monitor response times and error rates
```

### Database Performance

```bash
# Check query performance
psql $DATABASE_URL << 'EOF'
EXPLAIN ANALYZE
SELECT * FROM messages
WHERE conversation_id = 1
ORDER BY created_at ASC
LIMIT 50;
EOF

# Verify indexes are being used
# Look for "Index Scan" in output (not "Seq Scan")
```

---

## Development Workflow

### Making Changes

1. **Update Specification**: Edit `specs/003-ai-chatbot/spec.md`
2. **Update Plan**: Edit `specs/003-ai-chatbot/plan.md`
3. **Run Tests**: Ensure all tests pass
4. **Commit Changes**: Use descriptive commit messages
5. **Create PR**: Follow project PR guidelines

### Adding New MCP Tools

```bash
# 1. Create tool file
touch backend/src/mcp/tools/new_tool.py

# 2. Define tool function
cat > backend/src/mcp/tools/new_tool.py << 'EOF'
from mcp import tool

@tool()
async def new_tool(user_id: str, param: str) -> dict:
    """Tool description."""
    # Implementation
    return {"status": "success"}
EOF

# 3. Register tool in MCP server
# Edit backend/src/mcp/server.py to import and register

# 4. Add tests
touch backend/tests/unit/test_new_tool.py

# 5. Update contracts
# Edit specs/003-ai-chatbot/contracts/mcp-tools.yaml
```

---

## Monitoring & Debugging

### Backend Logs

```bash
# View logs in real-time
tail -f backend/logs/app.log

# Filter for errors
tail -f backend/logs/app.log | grep ERROR

# View specific conversation
tail -f backend/logs/app.log | grep "conversation_id=123"
```

### Database Queries

```bash
# View recent conversations
psql $DATABASE_URL -c "SELECT id, user_id, created_at FROM conversations ORDER BY created_at DESC LIMIT 10;"

# View recent messages
psql $DATABASE_URL -c "SELECT id, conversation_id, role, LEFT(content, 50) as content_preview, created_at FROM messages ORDER BY created_at DESC LIMIT 20;"

# Count messages per conversation
psql $DATABASE_URL -c "SELECT conversation_id, COUNT(*) as message_count FROM messages GROUP BY conversation_id ORDER BY message_count DESC;"
```

### OpenAI API Usage

```bash
# Monitor API usage in OpenAI dashboard
# https://platform.openai.com/usage

# Track token usage per request
# Check backend logs for token counts
tail -f backend/logs/app.log | grep "tokens_used"
```

---

## Next Steps

After successful setup and testing:

1. ✅ Verify all manual tests pass
2. ✅ Run automated test suite
3. ✅ Perform load testing
4. ⏭️ **Run `/sp.tasks`** to generate implementation tasks
5. ⏭️ Begin implementation following task breakdown
6. ⏭️ Deploy to staging environment
7. ⏭️ Deploy to production

---

## Additional Resources

- **OpenAI ChatKit Docs**: https://platform.openai.com/docs/guides/chatkit
- **MCP SDK Docs**: https://github.com/modelcontextprotocol/python-sdk
- **OpenAI Agents SDK**: https://platform.openai.com/docs/guides/agents
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **Neon Docs**: https://neon.tech/docs

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review specification: `specs/003-ai-chatbot/spec.md`
3. Review plan: `specs/003-ai-chatbot/plan.md`
4. Check project documentation in `CLAUDE.md`
