<!--
Sync Impact Report:
Version change: N/A -> 1.0.0
List of modified principles:
- Added Principle 1: Natural Language Task Management
- Added Principle 2: MCP-Driven Operations
- Added Principle 3: Stateless Processing
- Added Principle 4: Secure User Isolation
- Added Principle 5: Persistent Conversation History
Added sections: Additional Constraints, Development Workflow
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/sp.constitution.md ✅ updated
Follow-up TODOs: None
-->
# Phase III – AI-Powered Todo Chatbot Constitution

## Core Principles

### Natural Language Task Management
All task management operations must be accessible through natural language interfaces. The chatbot interface serves as the primary interaction mechanism for users to create, read, update, and delete todo items using conversational commands.

### MCP-Driven Operations
All task operations must be implemented as MCP (Model Context Protocol) tools that AI agents can invoke. The system must expose CRUD operations for todos as discoverable tools that the AI agent can use for task management.

### Stateless Processing
The chat processing system must remain stateless, with conversation history stored persistently in the database. Each chat request must be processed independently without relying on server-side session state.

### Secure User Isolation
JWT authentication must be validated for all requests to ensure secure user data isolation. Users can only access and modify their own tasks and conversations.

### Persistent Conversation History
Conversation history must be stored in the Neon PostgreSQL database and retrieved for context continuity across sessions. Users should be able to resume conversations with their previous context intact.

### MCP Tool Integration
All core functionality must be exposed as MCP tools following the official MCP SDK specification. AI agents must be able to discover and invoke these tools through the OpenAI Agents SDK.

## Additional Constraints
- Frontend must use OpenAI ChatKit for the chat interface
- Backend must use FastAPI framework
- AI reasoning must be handled through OpenAI Agents SDK
- MCP server must use the official MCP SDK
- Database must use Neon PostgreSQL with SQLModel ORM
- Authentication must use Better Auth JWT tokens
- Server must remain stateless with no session persistence

## Development Workflow
- All CRUD task actions must be exposed as MCP tools
- Chat endpoints must retrieve and store conversation history
- Authentication context must be validated for all requests
- All task operations must support natural language processing
- MCP tools must correctly execute all task operations
- Phase II features must remain fully functional after Phase III implementation

## Governance
All code changes must comply with these constitutional principles. New features must follow the natural language interface paradigm and expose functionality through MCP tools. Any changes to authentication or database access must maintain secure user isolation. The constitution may only be amended through a documented approval process with justification for changes.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
