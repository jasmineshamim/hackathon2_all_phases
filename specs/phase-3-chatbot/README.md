# Phase III: AI-Powered Todo Chatbot

**Status**: 🔄 Pending Implementation
**Required By**: See Hackathon II timeline
**Previous Phase**: Phase II (Web Application)

## Overview

This phase adds conversational AI capabilities to the todo application using:
- OpenAI ChatKit for the chat interface
- OpenAI Agents SDK for AI logic
- Model Context Protocol (MCP) for tool exposure
- Natural language understanding for task management

## Phase Goals

1. Create conversational interface for task management
2. Implement MCP server with task operation tools
3. Build stateless chat endpoint with history persistence
4. Enable natural language task commands
5. Integrate with Phase II backend

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend UI | OpenAI ChatKit |
| Backend Framework | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| Database | Neon Serverless PostgreSQL |
| ORM | SQLModel |
| Authentication | Better Auth + JWT |

## To Be Implemented

When ready to start this phase:

1. Review this placeholder document
2. Create feature specs in `specs/phase-3-chatbot/`
3. Create MCP server code in `phase-3-chatbot/backend/`
4. Create ChatKit UI in `phase-3-chatbot/frontend/`
5. Update CLAUDE.md for this phase

## Required MCP Tools

| Tool | Purpose |
|------|---------|
| `add_task` | Create a new task |
| `list_tasks` | Retrieve tasks with optional status filter |
| `complete_task` | Mark a task as complete |
| `delete_task` | Remove a task |
| `update_task` | Modify task title or description |

## Key Features to Spec

- [ ] Chat interface with OpenAI ChatKit
- [ ] MCP server exposing task tools
- [ ] OpenAI Agent for intent understanding
- [ ] Conversation history persistence
- [ ] Stateless chat endpoint

## Dependencies

- OpenAI API key
- OpenAI Platform account (for ChatKit domain allowlist)
- Phase II backend API

---

*This placeholder will be replaced with actual specifications when Phase III begins.*
