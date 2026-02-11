# Research: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08
**Phase**: Phase 0 - Research & Technology Decisions

## Overview

This document captures research findings and technology decisions for implementing a conversational AI chatbot interface for task management. The research focuses on integrating OpenAI ChatKit, MCP (Model Context Protocol) SDK, and OpenAI Agents SDK into the existing Phase II architecture.

## Research Areas

### 1. OpenAI ChatKit Integration

**Research Question**: How to integrate OpenAI ChatKit with existing Better Auth JWT authentication?

**Findings**:
- OpenAI ChatKit requires domain allowlist configuration in OpenAI platform settings
- ChatKit accepts custom authentication via JWT tokens passed in headers
- Domain key must be obtained after adding production domain to allowlist
- Local development (localhost) typically works without domain configuration
- ChatKit provides built-in message display, input handling, and conversation UI

**Implementation Approach**:
```typescript
// Frontend configuration
import { ChatKit } from '@openai/chatkit';

const chatConfig = {
  apiEndpoint: '/api/{user_id}/chat',
  headers: {
    'Authorization': `Bearer ${jwtToken}`
  },
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY
};
```

**Key Decisions**:
- Use ChatKit's default UI components (no customization needed for MVP)
- Pass JWT token in Authorization header for each chat request
- Configure domain allowlist before production deployment

**References**:
- OpenAI ChatKit Documentation: https://platform.openai.com/docs/guides/chatkit
- Domain Allowlist Setup: https://platform.openai.com/settings/organization/security/domain-allowlist

---

### 2. MCP Server Architecture

**Research Question**: How to structure MCP server with Official MCP SDK in FastAPI backend?

**Findings**:
- Official MCP SDK provides Python decorators for tool definitions
- Tools are defined as async functions with typed parameters
- MCP server can run as embedded module within FastAPI (no separate process needed)
- Tool schemas are automatically generated from function signatures and docstrings
- Error handling in tools should return structured error objects

**Implementation Approach**:
```python
# backend/src/mcp/server.py
from mcp import MCPServer, Tool

mcp_server = MCPServer()

@mcp_server.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = None
) -> dict:
    """
    Create a new task for the user.

    Args:
        user_id: The authenticated user's ID
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        dict: {task_id: int, status: str, title: str}
    """
    # Implementation
    pass
```

**Key Decisions**:
- Integrate MCP server as FastAPI module (not separate microservice)
- Use async functions for all tools to support concurrent requests
- Include user_id parameter in all tools for security filtering
- Return structured responses with status, data, and error fields

**References**:
- Official MCP SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP Protocol Specification: https://modelcontextprotocol.io/docs

---

### 3. OpenAI Agents SDK

**Research Question**: How to configure OpenAI Agents SDK for task management conversations?

**Findings**:
- Agents SDK requires system prompt defining agent behavior and available tools
- Agent automatically selects and invokes appropriate tools based on user intent
- Conversation context is maintained through message history array
- Agent supports both streaming and non-streaming responses
- Tool results are automatically incorporated into agent's response generation

**Implementation Approach**:
```python
# backend/src/agents/chat_agent.py
from openai import OpenAI
from openai.agents import Agent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
You are a helpful task management assistant. You help users manage their todo list through natural language conversation.

Available operations:
- Create tasks: "Add task to...", "I need to remember to..."
- List tasks: "Show me my tasks", "What's pending?"
- Complete tasks: "Mark task X as complete", "I finished..."
- Update tasks: "Change task X to...", "Update task..."
- Delete tasks: "Delete task X", "Remove the..."

Always confirm actions and provide clear feedback.
"""

agent = Agent(
    model="gpt-4",
    system_prompt=system_prompt,
    tools=[add_task, list_tasks, complete_task, delete_task, update_task]
)
```

**Key Decisions**:
- Use GPT-4 model for better intent understanding (can downgrade to GPT-3.5-turbo for cost)
- Non-streaming responses for MVP (simpler implementation)
- Include conversation history in each request for context
- System prompt emphasizes confirmation and clear feedback

**References**:
- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents
- Agent Configuration: https://platform.openai.com/docs/api-reference/agents

---

### 4. Stateless Chat Endpoint Design

**Research Question**: How to implement stateless chat endpoint with database-persisted conversation state?

**Findings**:
- Stateless design requires fetching conversation history from database on each request
- Message array must be constructed: system prompt + history + new message
- Database transactions ensure message persistence before response
- Concurrent requests from same user should be queued or handled with optimistic locking
- Conversation history should be paginated for performance (limit to last 50 messages)

**Implementation Approach**:
```python
# backend/src/api/routes/chat.py
@router.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    token: str = Depends(verify_jwt_token)
):
    # 1. Validate user_id matches token
    if token.user_id != user_id:
        raise HTTPException(401, "Unauthorized")

    # 2. Get or create conversation
    conversation = await get_or_create_conversation(user_id, request.conversation_id)

    # 3. Fetch conversation history (last 50 messages)
    history = await get_conversation_history(conversation.id, limit=50)

    # 4. Store user message
    await store_message(conversation.id, user_id, "user", request.message)

    # 5. Build message array for agent
    messages = build_message_array(history, request.message)

    # 6. Invoke agent
    response = await agent.run(messages)

    # 7. Store assistant message
    await store_message(conversation.id, user_id, "assistant", response.content)

    # 8. Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=response.content,
        tool_calls=response.tool_calls
    )
```

**Key Decisions**:
- Fetch last 50 messages for context (balance between context and performance)
- Store messages before and after agent invocation (audit trail)
- Return tool_calls in response for transparency
- Use database transactions to ensure consistency

**References**:
- FastAPI Async Patterns: https://fastapi.tiangolo.com/async/
- SQLModel Async: https://sqlmodel.tiangolo.com/tutorial/async/

---

### 5. Database Schema Design

**Research Question**: How to design Conversation and Message tables for optimal performance?

**Findings**:
- Conversation table should be lightweight (just metadata)
- Message table will grow large - needs proper indexing
- Foreign key relationships ensure referential integrity
- Indexes on user_id, conversation_id, and created_at critical for performance
- Consider partitioning messages table by date for very large datasets (future optimization)

**Implementation Approach**:
```sql
-- Conversation table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Message table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_user_id ON messages(user_id);
```

**Key Decisions**:
- Use SERIAL for auto-incrementing IDs
- CASCADE delete to clean up messages when conversation deleted
- Index on conversation_id for fast history retrieval
- Index on created_at for chronological ordering
- Store role as VARCHAR with CHECK constraint for data integrity

**References**:
- PostgreSQL Indexing: https://www.postgresql.org/docs/current/indexes.html
- Neon Database Best Practices: https://neon.tech/docs/guides/performance

---

## Technology Stack Validation

### Frontend Stack
- ✅ **Next.js 16+ (App Router)**: Confirmed compatible with OpenAI ChatKit
- ✅ **OpenAI ChatKit**: Official library, well-documented, meets requirements
- ✅ **Better Auth JWT**: Compatible with ChatKit custom authentication
- ✅ **Tailwind CSS**: Existing styling system, no conflicts

### Backend Stack
- ✅ **Python 3.11+**: Required for Official MCP SDK and OpenAI Agents SDK
- ✅ **FastAPI**: Async support, compatible with MCP server integration
- ✅ **Official MCP SDK**: Python package available, active development
- ✅ **OpenAI Agents SDK**: Stable API, good documentation
- ✅ **SQLModel**: Async support, compatible with Neon PostgreSQL

### Database
- ✅ **Neon Serverless PostgreSQL**: Supports required features (foreign keys, indexes, transactions)
- ✅ **Connection Pooling**: Built-in support for concurrent connections
- ✅ **Alembic Migrations**: Compatible with SQLModel and Neon

---

## Risk Assessment

### High Risk
1. **OpenAI API Rate Limits**
   - **Mitigation**: Implement rate limiting on chat endpoint, monitor usage
   - **Fallback**: Queue requests during high load

2. **OpenAI API Costs**
   - **Mitigation**: Use GPT-3.5-turbo for development, GPT-4 for production
   - **Monitoring**: Track token usage per request

### Medium Risk
1. **Conversation History Size**
   - **Mitigation**: Limit to last 50 messages, implement pagination
   - **Future**: Archive old conversations

2. **Concurrent Request Handling**
   - **Mitigation**: Use database transactions, implement request queuing if needed
   - **Testing**: Load test with 100 concurrent users

### Low Risk
1. **MCP Tool Errors**
   - **Mitigation**: Comprehensive error handling in each tool
   - **Testing**: Unit tests for all error scenarios

2. **ChatKit Domain Configuration**
   - **Mitigation**: Document setup process, test before production
   - **Fallback**: Local development works without domain key

---

## Performance Benchmarks

### Target Metrics
- Chat response time: <2 seconds (simple queries)
- AI agent processing: <3 seconds (including tool invocations)
- Conversation history load: <1 second
- Database query latency: <100ms
- Support 100 concurrent chat sessions

### Optimization Strategies
1. **Database**: Proper indexing, connection pooling, query optimization
2. **API**: Async operations, caching frequently accessed data
3. **Agent**: Limit conversation history to 50 messages
4. **Frontend**: Optimistic UI updates, loading states

---

## Security Considerations

### Authentication & Authorization
- ✅ JWT token validation on all requests
- ✅ User ID verification (token.user_id == path.user_id)
- ✅ All MCP tools filter by authenticated user_id

### Data Privacy
- ✅ Conversation data scoped to user
- ✅ No cross-user data leakage
- ✅ Secure OpenAI API key storage (environment variables)

### Input Validation
- ✅ Validate message length (max 2000 characters)
- ✅ Sanitize user inputs before database storage
- ✅ Validate tool parameters in MCP tools

---

## Dependencies & Versions

### Frontend
```json
{
  "@openai/chatkit": "^1.0.0",
  "next": "^16.0.0",
  "react": "^18.0.0",
  "better-auth": "^1.0.0"
}
```

### Backend
```txt
fastapi==0.109.0
uvicorn==0.27.0
sqlmodel==0.0.14
openai==1.10.0
mcp-sdk==0.1.0
pydantic==2.5.0
alembic==1.13.0
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
```

---

## Next Steps

1. ✅ Research completed - All technology decisions validated
2. ⏭️ **Phase 1**: Generate data-model.md with entity definitions
3. ⏭️ **Phase 1**: Create API contracts (chat-api.yaml, mcp-tools.yaml)
4. ⏭️ **Phase 1**: Generate quickstart.md with setup instructions
5. ⏭️ **Phase 2**: Run `/sp.tasks` to break down implementation into tasks

---

## Conclusion

All research areas have been investigated and technology decisions validated. The proposed architecture is feasible with the specified technology stack. Key risks have been identified with mitigation strategies. The system is ready to proceed to Phase 1 (Design & Contracts).
