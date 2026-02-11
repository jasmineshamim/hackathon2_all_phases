# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

**Note**: This plan outlines the technical architecture for implementing a conversational AI chatbot interface for task management using MCP (Model Context Protocol) and OpenAI Agents SDK.

## Summary

This plan implements a conversational AI chatbot that allows users to manage tasks through natural language. The system uses OpenAI ChatKit for the frontend interface, FastAPI for the backend chat endpoint, an MCP server to expose task operations as tools, and OpenAI Agents SDK to process natural language and invoke appropriate tools. The architecture is stateless with all conversation state persisted to Neon PostgreSQL database, enabling conversation resumption after server restarts.

## Technical Context

**Language/Version**:
- Frontend: TypeScript, Next.js 16+ (App Router)
- Backend: Python 3.11+
- MCP Server: Python 3.11+ with Official MCP SDK

**Primary Dependencies**:
- Frontend: OpenAI ChatKit, Next.js, React, Tailwind CSS, Better Auth (JWT)
- Backend: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, httpx
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens

**Storage**: Neon Serverless PostgreSQL with new tables:
- conversations (id, user_id, created_at, updated_at)
- messages (id, conversation_id, user_id, role, content, created_at)
- Existing: tasks, users (from Phase II)

**Testing**:
- Frontend: Jest, React Testing Library, Cypress E2E
- Backend: pytest, pytest-asyncio, httpx for API testing
- MCP Tools: Unit tests for each tool function
- Integration: End-to-end conversation flow tests

**Target Platform**:
- Web browsers (Chrome, Firefox, Safari, Edge)
- Responsive design (mobile, tablet, desktop)
- Backend: Linux server (containerized)

**Project Type**: web (monorepo with frontend and backend)

**Performance Goals**:
- Chat response time: <2 seconds for simple queries
- AI agent processing: <3 seconds including tool invocations
- Conversation history load: <1 second
- Support 100 concurrent chat sessions
- Database query latency: <100ms

**Constraints**:
- Must use OpenAI ChatKit (not custom chat UI)
- Must use Official MCP SDK for tool definitions
- Must remain stateless (no in-memory session storage)
- Must integrate with existing Phase II authentication (JWT)
- Must filter all operations by authenticated user
- OpenAI API rate limits and costs
- Neon database connection limits

**Scale/Scope**:
- 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- 1 chat endpoint (POST /api/{user_id}/chat)
- 2 new database models (Conversation, Message)
- Support for unlimited conversation history per user
- Natural language variations for each operation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on project requirements and best practices:

**✅ PASS - Core Requirements:**
- Integrates with existing Phase II authentication and task management
- Follows spec-driven development workflow
- Uses specified technology stack (OpenAI ChatKit, FastAPI, MCP SDK, OpenAI Agents SDK)
- Maintains stateless architecture with database persistence
- Implements all Basic Level task operations conversationally

**✅ PASS - Testing Requirements:**
- Unit tests for MCP tools
- Integration tests for chat endpoint
- End-to-end tests for conversation flows
- API contract tests

**✅ PASS - Security Requirements:**
- JWT token validation on all requests
- User-scoped data access (filter by user_id)
- No sensitive data in conversation logs
- Secure OpenAI API key management

**✅ PASS - Performance Requirements:**
- Response time targets defined (<2s for queries, <3s for AI processing)
- Scalability target (100 concurrent sessions)
- Database query optimization

**⚠️ CONSIDERATION - Complexity:**
- Adding 3 new major components (ChatKit UI, MCP Server, Agents SDK integration)
- Justified by hackathon Phase III requirements
- Each component serves distinct purpose in conversational architecture

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Technology research and decisions
├── data-model.md        # Phase 1 output - Database schema and entities
├── quickstart.md        # Phase 1 output - Setup and testing guide
├── contracts/           # Phase 1 output - API contracts
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.yaml   # MCP tool definitions
├── checklists/          # Validation checklists
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)

backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # Conversation SQLModel
│   │   ├── message.py           # Message SQLModel
│   │   └── task.py              # Existing Task model (Phase II)
│   ├── mcp/
│   │   ├── server.py            # MCP server initialization
│   │   ├── tools/
│   │   │   ├── add_task.py      # MCP tool: add_task
│   │   │   ├── list_tasks.py    # MCP tool: list_tasks
│   │   │   ├── complete_task.py # MCP tool: complete_task
│   │   │   ├── delete_task.py   # MCP tool: delete_task
│   │   │   └── update_task.py   # MCP tool: update_task
│   │   └── schemas.py           # Tool input/output schemas
│   ├── agents/
│   │   ├── chat_agent.py        # OpenAI Agents SDK integration
│   │   └── prompts.py           # System prompts for agent
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py          # POST /api/{user_id}/chat
│   │   │   └── tasks.py         # Existing task routes (Phase II)
│   │   └── middleware/
│   │       └── auth.py          # JWT validation middleware
│   ├── services/
│   │   ├── conversation_service.py  # Conversation CRUD operations
│   │   ├── message_service.py       # Message CRUD operations
│   │   └── task_service.py          # Existing task service (Phase II)
│   ├── db/
│   │   ├── database.py          # Database connection
│   │   └── migrations/          # Alembic migrations
│   │       └── add_conversation_tables.py
│   └── main.py                  # FastAPI app entry point
├── tests/
│   ├── unit/
│   │   ├── test_mcp_tools.py    # Unit tests for each MCP tool
│   │   ├── test_chat_agent.py   # Agent behavior tests
│   │   └── test_services.py     # Service layer tests
│   ├── integration/
│   │   ├── test_chat_endpoint.py    # Chat API integration tests
│   │   └── test_conversation_flow.py # End-to-end conversation tests
│   └── fixtures/
│       └── sample_conversations.json
├── requirements.txt
└── pyproject.toml

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx             # Chat interface page (OpenAI ChatKit)
│   ├── dashboard/
│   │   ├── page.tsx             # Existing dashboard (Phase II)
│   │   └── tasks/
│   │       └── page.tsx         # Existing task form (Phase II)
│   └── auth/                    # Existing auth pages (Phase II)
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx    # OpenAI ChatKit wrapper
│   │   ├── MessageList.tsx      # Conversation history display
│   │   └── ChatInput.tsx        # Message input component
│   └── Navbar.tsx               # Updated with chat link
├── lib/
│   ├── api-client.ts            # Existing API client (Phase II)
│   ├── chat-client.ts           # Chat API client
│   └── openai-config.ts         # OpenAI ChatKit configuration
├── hooks/
│   └── useChat.ts               # Custom hook for chat functionality
└── tests/
    └── e2e/
        └── chat-flow.cy.ts      # Cypress E2E tests for chat

database/
└── migrations/
    └── 003_add_conversation_tables.sql  # SQL migration for new tables
```

**Structure Decision**: Selected web application structure (monorepo) with separate frontend and backend directories. This maintains consistency with Phase II architecture while adding new chat-specific components. The MCP server is integrated within the backend as a module rather than a separate service to simplify deployment and reduce latency.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Three major new components (ChatKit, MCP, Agents SDK) | Hackathon Phase III requirements mandate conversational interface with MCP architecture | Direct API calls without MCP would not meet hackathon specifications; custom chat UI would violate "must use OpenAI ChatKit" constraint |
| Stateless architecture with database persistence | Required for scalability and conversation resumption after server restart | In-memory session storage would fail conversation persistence requirement and limit horizontal scaling |
| Separate MCP tool module | MCP SDK requires tool definitions as separate callable functions | Inline tool definitions would violate MCP protocol standards and reduce testability |

## Phase 0: Research & Technology Decisions

### Research Areas

1. **OpenAI ChatKit Integration**
   - Domain allowlist configuration requirements
   - Authentication flow with Better Auth JWT
   - Message formatting and display customization
   - Error handling and loading states

2. **MCP Server Architecture**
   - Official MCP SDK tool definition patterns
   - Tool input/output schema design
   - Error handling in tool functions
   - Integration with FastAPI application

3. **OpenAI Agents SDK**
   - Agent initialization and configuration
   - System prompt design for task management
   - Tool invocation patterns
   - Conversation context management
   - Streaming vs non-streaming responses

4. **Stateless Chat Endpoint Design**
   - Conversation history retrieval patterns
   - Message array construction for agent
   - Database transaction management
   - Concurrent request handling

5. **Database Schema Design**
   - Conversation and Message table relationships
   - Indexing strategy for performance
   - Conversation history pagination
   - Data retention policies

### Technology Decisions

**Decision 1: MCP Server as Backend Module**
- **Rationale**: Integrating MCP server within FastAPI backend reduces network latency and simplifies deployment
- **Alternatives Considered**: Separate MCP server microservice
- **Rejected Because**: Additional network hop would increase response time; deployment complexity not justified for 5 tools

**Decision 2: Non-Streaming Chat Responses**
- **Rationale**: Simpler implementation for MVP; meets <3s response time requirement
- **Alternatives Considered**: Streaming responses with Server-Sent Events
- **Rejected Because**: Added complexity not required for Phase III; can be added later if needed

**Decision 3: Single Conversation per User Session**
- **Rationale**: Simplifies UI and meets hackathon requirements
- **Alternatives Considered**: Multiple concurrent conversations
- **Rejected Because**: Not required by spec; adds UI complexity

**Decision 4: Tool Results Included in Response**
- **Rationale**: Transparency for debugging and user understanding
- **Alternatives Considered**: Hide tool invocations from user
- **Rejected Because**: Spec requires "tool_calls" in response; helpful for user feedback

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Key Entities:**
- Conversation: Chat session container
- Message: Individual messages (user/assistant)
- Task: Existing entity from Phase II
- User: Existing entity from Phase II

### API Contracts

See [contracts/chat-api.yaml](./contracts/chat-api.yaml) for OpenAPI specification.

**Primary Endpoint:**
- POST /api/{user_id}/chat
  - Request: { conversation_id?: int, message: string }
  - Response: { conversation_id: int, response: string, tool_calls: array }

See [contracts/mcp-tools.yaml](./contracts/mcp-tools.yaml) for MCP tool definitions.

**MCP Tools:**
1. add_task(user_id, title, description?)
2. list_tasks(user_id, status?)
3. complete_task(user_id, task_id)
4. delete_task(user_id, task_id)
5. update_task(user_id, task_id, title?, description?)

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup and testing instructions.

## Architecture Diagrams

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           OpenAI ChatKit Interface                         │ │
│  │  - Message display                                         │ │
│  │  - Input handling                                          │ │
│  │  - Conversation history                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              │ POST /api/{user_id}/chat          │
│                              │ Authorization: Bearer <JWT>       │
│                              ▼                                   │
└─────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────┐
│                         Backend (FastAPI)                         │
│  ┌───────────────────────────▼────────────────────────────────┐  │
│  │                    Chat Endpoint                           │  │
│  │  1. Validate JWT token                                     │  │
│  │  2. Fetch conversation history from DB                     │  │
│  │  3. Build message array (history + new message)            │  │
│  │  4. Store user message in DB                               │  │
│  └────────────────────────────┬───────────────────────────────┘  │
│                               │                                   │
│  ┌────────────────────────────▼───────────────────────────────┐  │
│  │              OpenAI Agents SDK                             │  │
│  │  - Process natural language                                │  │
│  │  - Determine intent                                        │  │
│  │  - Select appropriate MCP tool(s)                          │  │
│  │  - Invoke tool(s) with parameters                          │  │
│  └────────────────────────────┬───────────────────────────────┘  │
│                               │                                   │
│  ┌────────────────────────────▼───────────────────────────────┐  │
│  │                    MCP Server                              │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │  Tool: add_task(user_id, title, description)         │  │  │
│  │  │  Tool: list_tasks(user_id, status)                   │  │  │
│  │  │  Tool: complete_task(user_id, task_id)               │  │  │
│  │  │  Tool: delete_task(user_id, task_id)                 │  │  │
│  │  │  Tool: update_task(user_id, task_id, title, desc)    │  │  │
│  │  └──────────────────────────┬───────────────────────────┘  │  │
│  │                             │                               │  │
│  │                             │ Database Operations           │  │
│  │                             ▼                               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                               │                                   │
└───────────────────────────────┼───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                  Neon PostgreSQL Database                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Tables:                                                    │  │
│  │  - conversations (id, user_id, created_at, updated_at)     │  │
│  │  - messages (id, conversation_id, user_id, role, content)  │  │
│  │  - tasks (existing from Phase II)                          │  │
│  │  - users (existing from Phase II)                          │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

### Conversation Flow (Stateless Request Cycle)

```
1. User sends message via ChatKit
   ↓
2. Frontend: POST /api/{user_id}/chat
   Headers: Authorization: Bearer <JWT>
   Body: { conversation_id: 123, message: "Add task to buy groceries" }
   ↓
3. Backend: Validate JWT token
   ↓
4. Backend: Fetch conversation history from database
   SELECT * FROM messages WHERE conversation_id = 123 ORDER BY created_at
   ↓
5. Backend: Build message array for agent
   [
     { role: "system", content: "You are a task management assistant..." },
     { role: "user", content: "Show me my tasks" },
     { role: "assistant", content: "Here are your tasks: ..." },
     { role: "user", content: "Add task to buy groceries" }  ← new message
   ]
   ↓
6. Backend: Store user message in database
   INSERT INTO messages (conversation_id, user_id, role, content, created_at)
   ↓
7. Backend: Pass message array to OpenAI Agents SDK
   ↓
8. Agent: Analyze intent → Determine "add_task" tool needed
   ↓
9. Agent: Invoke MCP tool: add_task(user_id="user123", title="Buy groceries")
   ↓
10. MCP Tool: Execute database operation
    INSERT INTO tasks (user_id, title, completed, created_at)
    ↓
11. MCP Tool: Return result
    { task_id: 456, status: "created", title: "Buy groceries" }
    ↓
12. Agent: Generate natural language response
    "I've added 'Buy groceries' to your task list."
    ↓
13. Backend: Store assistant message in database
    INSERT INTO messages (conversation_id, user_id, role, content, created_at)
    ↓
14. Backend: Return response to frontend
    {
      conversation_id: 123,
      response: "I've added 'Buy groceries' to your task list.",
      tool_calls: [{ tool: "add_task", parameters: {...}, result: {...} }]
    }
    ↓
15. Frontend: Display response in ChatKit
    ↓
16. Server: Ready for next request (NO STATE HELD)
```

## Security Considerations

1. **JWT Token Validation**: All chat requests must include valid JWT token in Authorization header
2. **User Scoping**: All MCP tools filter operations by user_id to prevent cross-user data access
3. **Input Sanitization**: Validate and sanitize all user inputs before processing
4. **OpenAI API Key**: Store securely in environment variables, never expose to frontend
5. **Rate Limiting**: Implement rate limiting on chat endpoint to prevent abuse
6. **SQL Injection Prevention**: Use SQLModel parameterized queries
7. **Conversation Privacy**: Ensure users can only access their own conversations

## Performance Optimization

1. **Database Indexing**:
   - Index on conversations.user_id
   - Index on messages.conversation_id
   - Index on messages.created_at for chronological ordering

2. **Conversation History Pagination**:
   - Limit initial load to last 50 messages
   - Implement "load more" for older messages

3. **Connection Pooling**:
   - Configure SQLModel connection pool for concurrent requests
   - Neon serverless handles connection scaling

4. **Caching**:
   - Consider caching frequently accessed task lists
   - Cache user authentication state

5. **Async Operations**:
   - Use async/await throughout FastAPI endpoints
   - Async database queries with SQLModel

## Error Handling Strategy

1. **OpenAI API Errors**:
   - Catch rate limit errors → Return friendly message
   - Catch timeout errors → Retry with exponential backoff
   - Catch invalid request errors → Log and return generic error

2. **Database Errors**:
   - Connection failures → Return "Service temporarily unavailable"
   - Query errors → Log details, return generic error to user

3. **MCP Tool Errors**:
   - Task not found → Return specific error message
   - Invalid parameters → Return validation error with guidance

4. **Agent Errors**:
   - Intent unclear → Ask clarifying question
   - Tool invocation failed → Inform user and suggest alternative

## Testing Strategy

1. **Unit Tests**:
   - Each MCP tool function
   - Conversation and message service methods
   - Agent prompt generation

2. **Integration Tests**:
   - Chat endpoint with mocked OpenAI API
   - Database operations with test database
   - Full conversation flow

3. **E2E Tests**:
   - Complete user journey: login → chat → create task → verify
   - Conversation persistence across sessions
   - Error scenarios

4. **Performance Tests**:
   - Load testing with 100 concurrent users
   - Response time validation (<2s, <3s targets)

## Deployment Considerations

1. **Environment Variables**:
   - OPENAI_API_KEY
   - DATABASE_URL (Neon connection string)
   - BETTER_AUTH_SECRET (for JWT validation)
   - OPENAI_DOMAIN_KEY (for ChatKit)

2. **Database Migrations**:
   - Run Alembic migrations to create conversation tables
   - Verify indexes are created

3. **Frontend Deployment**:
   - Add chat domain to OpenAI allowlist
   - Configure NEXT_PUBLIC_OPENAI_DOMAIN_KEY

4. **Backend Deployment**:
   - Ensure FastAPI server has access to OpenAI API
   - Configure CORS for frontend domain

## Next Steps

After this plan is approved:

1. **Run `/sp.tasks`** to generate actionable task breakdown
2. **Implement Phase 0**: Research and validate technology choices
3. **Implement Phase 1**: Create data models and API contracts
4. **Implement Phase 2**: Build and test each component
5. **Integration Testing**: Verify end-to-end conversation flow
6. **Deployment**: Deploy to Vercel (frontend) and production server (backend)

## Architectural Decision Records (ADR)

📋 **Architectural decisions detected**:
1. MCP Server as Backend Module (vs separate microservice)
2. Non-Streaming Chat Responses (vs streaming)
3. Single Conversation per Session (vs multiple concurrent)
4. Stateless Architecture with Database Persistence (vs in-memory sessions)

Document these decisions? Run `/sp.adr <decision-title>` for each significant decision.
