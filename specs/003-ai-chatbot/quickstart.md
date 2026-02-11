# Quick Start Guide: Phase III – AI-Powered Todo Chatbot

**Feature**: Phase III – AI-Powered Todo Chatbot
**Date**: 2026-02-07
**Author**: Claude Code

## Overview

This guide provides step-by-step instructions for setting up, running, and testing the AI-powered todo chatbot application. Follow these steps to get the application running locally and verify all functionality.

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed
- Access to Neon PostgreSQL account
- OpenAI API key
- Better Auth configuration

## Environment Setup

### 1. Clone and Navigate to Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Create Backend Environment File

```bash
cd backend
touch .env
```

Add the following to `backend/.env`:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=http://localhost:3000
```

### 3. Create Frontend Environment File

```bash
cd ../frontend
touch .env.local
```

Add the following to `frontend/.env.local`:

```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_API_KEY=your-openai-api-key
```

## Backend Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install poetry
poetry install
```

### 2. Run Database Migrations

```bash
poetry run python -m database.migrations.create_tables
```

### 3. Start Backend Server

```bash
poetry run uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

## Frontend Setup

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Start Frontend Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## MCP Server Setup

### 1. Install MCP Server Dependencies

```bash
cd mcp-server
pip install poetry
poetry install
```

### 2. Start MCP Server

```bash
poetry run python -m mcp_server.main
```

The MCP server will be available at `http://localhost:8001`.

## Testing Functionality

### 1. Verify Basic Setup

1. Navigate to `http://localhost:3000`
2. Verify the application loads without errors
3. Check that API endpoints are accessible at `http://localhost:8000/docs`

### 2. User Registration and Login

1. Click "Sign Up" and create a new account
2. Verify you can log in with the created credentials
3. Confirm JWT token is properly stored and used for API requests

### 3. Todo Operations via Chat Interface

1. Navigate to the chat interface
2. Test adding a task with a natural language command like "Add a task to buy groceries"
3. Verify the task appears in your task list
4. Test viewing tasks with "Show me my tasks"
5. Test updating a task with "Update task 1 to say buy groceries and milk"
6. Test marking complete with "Mark task 1 as complete"
7. Test deleting with "Delete task 1"

### 4. MCP Tool Invocation

1. Verify that the AI agent can discover the MCP tools
2. Check that tool invocations are properly logged
3. Confirm that tool responses are formatted correctly

### 5. Conversation History

1. Start a conversation and close the browser
2. Reopen and verify your conversation history is preserved
3. Check that the history is associated with the correct user

### 6. Multi-user Isolation

1. Log out and create a second user account
2. Add tasks for the second user
3. Verify the first user cannot see the second user's tasks
4. Verify the second user cannot see the first user's tasks

## API Testing

### 1. Test Authentication Endpoints

```bash
# Test registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepassword"}'

# Test protected endpoint
curl -X GET http://localhost:8000/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 2. Test Todo Endpoints

```bash
# Create a todo
curl -X POST http://localhost:8000/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test description", "priority": "medium"}'

# Get todos
curl -X GET http://localhost:8000/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 3. Test Chat Endpoint

```bash
# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify Neon PostgreSQL connection string is correct
   - Check that the database is properly created in Neon
   - Confirm SSL mode is set to require

2. **Authentication Fails**
   - Verify JWT secret is consistent between frontend and backend
   - Check that Better Auth is properly configured
   - Confirm environment variables are set correctly

3. **MCP Tools Not Discoverable**
   - Ensure MCP server is running
   - Verify the connection between AI agent and MCP server
   - Check that tools are properly registered

4. **Frontend Cannot Connect to Backend**
   - Verify CORS settings in FastAPI
   - Check that backend is running on the expected port
   - Confirm API base URL is set correctly in frontend

### Debug Commands

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check database connection
poetry run python -c "from database.models import engine; print('DB connected')"

# Check if MCP server is running
curl http://localhost:8001/health
```

## Production Deployment Notes

1. **Environment Variables**: Ensure production secrets are properly configured
2. **Database**: Use production-ready Neon PostgreSQL configuration
3. **Authentication**: Enable production authentication settings
4. **SSL**: Ensure HTTPS is enforced in production
5. **Monitoring**: Set up logging and monitoring for production usage