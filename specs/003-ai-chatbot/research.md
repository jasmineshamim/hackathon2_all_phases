# Research: Phase III – AI-Powered Todo Chatbot

**Feature**: Phase III – AI-Powered Todo Chatbot
**Date**: 2026-02-07
**Author**: Claude Code

## Overview

This document captures the research findings for implementing the AI-powered todo chatbot with MCP (Model Context Protocol) tools. It addresses all "NEEDS CLARIFICATION" items from the technical context and provides decision rationales for the technology stack and architecture.

## Key Decisions

### 1. Natural Language Processing Approach
- **Decision**: Use OpenAI Agents SDK for natural language understanding and task execution
- **Rationale**: The OpenAI Agents SDK provides robust natural language processing capabilities and integrates well with MCP tools. It handles intent recognition, entity extraction, and task orchestration.
- **Alternatives considered**:
  - Custom NLP with spaCy/transformers: Requires more development effort
  - Rule-based parsing: Limited flexibility and scalability

### 2. MCP Tool Implementation
- **Decision**: Implement MCP tools using the official MCP SDK for Python
- **Rationale**: MCP tools enable the AI agent to discover and execute specific functions. The official SDK ensures compatibility and follows best practices for tool registration and invocation.
- **Alternatives considered**:
  - Function calling without MCP: Less standardized approach
  - GraphQL mutations: Would require separate GraphQL layer

### 3. Frontend Technology
- **Decision**: Use OpenAI ChatKit for the chat interface
- **Rationale**: Provides a ready-made chat interface optimized for AI interactions with proper message threading and user experience patterns.
- **Alternatives considered**:
  - Custom chat UI with React: Requires more UI development
  - Generic chat libraries: Less optimized for AI agents

### 4. Backend Framework
- **Decision**: FastAPI for the backend API
- **Rationale**: FastAPI provides excellent performance, automatic API documentation, and strong typing. It's well-suited for serving both traditional REST APIs and MCP endpoints.
- **Alternatives considered**:
  - Flask: Less performant and lacks automatic documentation
  - Django: Overkill for this use case

### 5. Database and ORM
- **Decision**: Neon PostgreSQL with SQLModel ORM
- **Rationale**: Neon provides serverless PostgreSQL with great performance and scaling. SQLModel combines SQLAlchemy and Pydantic for clean model definitions with validation.
- **Alternatives considered**:
  - SQLite: Insufficient for multi-user scenario
  - MongoDB: No need for document flexibility
  - Raw SQL with asyncpg: Missing ORM benefits

### 6. Authentication System
- **Decision**: Better Auth with JWT tokens
- **Rationale**: Better Auth provides a comprehensive authentication solution with built-in JWT support, social logins, and session management while being easy to integrate with FastAPI.
- **Alternatives considered**:
  - Custom JWT implementation: More security risks
  - Auth0/Clerk: More complex setup and potential vendor lock-in

## Architecture Patterns

### MCP Tool Registration
- Tools are registered with the MCP server at startup
- Each tool corresponds to a specific todo operation (create, read, update, delete, toggle status)
- Tools include proper input validation and error handling

### Stateless Processing
- Server maintains no session state between requests
- All conversation context is stored in the database
- JWT tokens provide authentication context for each request

### Multi-user Data Isolation
- All database queries include user_id filters
- JWT tokens contain user identity information
- MCP tools automatically filter results by authenticated user

## Integration Points

### AI Agent ↔ MCP Tools
- The AI agent discovers available tools via MCP protocol
- Natural language is converted to structured tool calls
- Tool responses are formatted for natural language response generation

### Frontend ↔ Backend
- Chat interface communicates via REST APIs
- Authentication headers include JWT tokens
- Real-time updates via WebSocket connections (if needed)

### Database ↔ Services
- SQLModel provides typed model definitions
- Async database operations for performance
- Connection pooling for scalability

## Security Considerations

- JWT token validation on all authenticated endpoints
- User data isolation via database-level filtering
- Input validation on all API endpoints
- MCP tool parameter validation
- Rate limiting to prevent abuse

## Performance Considerations

- Async database operations to handle concurrent requests
- Caching for frequently accessed data
- Efficient database indexing for user-specific queries
- Optimized MCP tool response times

## Risks and Mitigations

### Natural Language Understanding Risks
- **Risk**: AI may misinterpret user intents
- **Mitigation**: Comprehensive error handling and user feedback loops

### Database Performance Risks
- **Risk**: High concurrency may affect database performance
- **Mitigation**: Proper indexing and connection pooling

### Security Risks
- **Risk**: Authentication bypass or data exposure
- **Mitigation**: Thorough user isolation and input validation