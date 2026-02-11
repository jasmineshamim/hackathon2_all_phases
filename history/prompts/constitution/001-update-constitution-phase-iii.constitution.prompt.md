---
id: 001
title: Update constitution for Phase III AI Chatbot
stage: constitution
date: 2026-02-07
surface: agent
model: Claude Sonnet 4.5
feature: Phase III – AI-Powered Todo Chatbot
branch: 001-auth-ui-enhancement
user: Lenovo
command: sp.constitution
labels: [constitution, phase-3, ai-chatbot, mcp, agents-sdk]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

Project: Phase III – AI-Powered Todo Chatbot (Agents + MCP Architecture)

Core principles:
- Natural language task management via chatbot interface
- AI agents must use MCP tools for all task operations
- Stateless chat processing with conversation history stored in database
- Secure user isolation using JWT authentication

Key standards:
- All CRUD task actions exposed as MCP tools
- Chat endpoint retrieves and stores conversation history
- Agents SDK handles reasoning and tool invocation
- All requests require authenticated user context

Constraints:
- Frontend: OpenAI ChatKit
- Backend: FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Database: Neon PostgreSQL (SQLModel ORM)
- Authentication: Better Auth JWT
- Server must remain stateless

Success criteria:
- Users manage todos using natural language
- MCP tools correctly execute all task operations
- Conversations persist across sessions
- Phase II features remain fully functional

## Response snapshot

Updated the project constitution to reflect the requirements for Phase III – AI-Powered Todo Chatbot. The new constitution includes core principles for natural language task management, MCP-driven operations, stateless processing, secure user isolation, and persistent conversation history. Additional constraints and development workflow guidelines were added to align with the technology stack (OpenAI ChatKit, FastAPI, Agents SDK, MCP SDK, Neon PostgreSQL with SQLModel, Better Auth JWT).

## Outcome

- ✅ Impact: Updated constitution document with 5 core principles and additional constraints
- 🧪 Tests: N/A (Documentation update)
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Proceed with feature specification for Phase III
- 🧠 Reflection: Constitution properly reflects Phase III requirements with MCP architecture

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create Phase III feature specification