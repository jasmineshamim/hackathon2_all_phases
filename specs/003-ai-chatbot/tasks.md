---
description: "Task list for Phase III – AI-Powered Todo Chatbot"
---

# Tasks: Phase III – AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only included if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Database**: `database/models/`
- Paths shown below follow the web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure (backend/src/models/, backend/src/services/, backend/src/api/)
- [X] T002 Create frontend directory structure (frontend/src/components/, frontend/src/pages/, frontend/src/services/)
- [X] T003 Create database directory structure (database/models/, database/migrations/)
- [X] T004 [P] Initialize Python backend with FastAPI dependencies in backend/pyproject.toml
- [X] T005 [P] Initialize Next.js frontend with TypeScript in frontend/package.json
- [X] T006 [P] Configure environment variables template in backend/.env.example
- [X] T007 [P] Configure environment variables template in frontend/.env.local.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Setup Neon PostgreSQL database connection in database/models/base.py
- [X] T009 [P] Create User model in database/models/user.py (if not exists from Phase II)
- [X] T010 [P] Create database migration framework in database/migrations/__init__.py
- [X] T011 Configure JWT validation middleware in backend/src/middleware/auth.py
- [X] T012 [P] Setup FastAPI main application with CORS in backend/src/main.py
- [X] T013 [P] Create authentication utilities in backend/src/utils/auth.py
- [X] T014 [P] Setup API error handling in backend/src/utils/errors.py
- [X] T015 Create base API router structure in backend/src/api/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - MCP Tool Integration (Priority: P2) 🎯

**Goal**: Expose all CRUD todo operations as MCP tools that AI agents can discover and invoke

**Independent Test**: MCP tools can be invoked directly and perform correct operations without the chat interface

**Why US2 before US1**: MCP tools are the foundation that US1 (chatbot) depends on

### Implementation for User Story 2

- [X] T016 [P] [US2] Create Todo model with priority field in database/models/todo.py
- [X] T017 [P] [US2] Create database migration for todos table in database/migrations/001_create_todos.py
- [X] T018 [US2] Implement TodoService with CRUD operations in backend/src/services/todo_service.py
- [X] T019 [US2] Install and configure MCP SDK in backend/pyproject.toml
- [X] T020 [US2] Create MCP tool for create-todo in backend/src/api/mcp_tools.py
- [X] T021 [P] [US2] Create MCP tool for list-todos in backend/src/api/mcp_tools.py
- [X] T022 [P] [US2] Create MCP tool for update-todo in backend/src/api/mcp_tools.py
- [X] T023 [P] [US2] Create MCP tool for delete-todo in backend/src/api/mcp_tools.py
- [X] T024 [P] [US2] Create MCP tool for toggle-todo-status in backend/src/api/mcp_tools.py
- [X] T025 [US2] Register all MCP tools with MCP server in backend/src/api/mcp_tools.py
- [X] T026 [US2] Create MCP tool discovery endpoint in backend/src/api/mcp_tools.py
- [X] T027 [US2] Add JWT authentication context to MCP tools in backend/src/api/mcp_tools.py

**Checkpoint**: At this point, MCP tools should be fully functional and testable independently

---

## Phase 4: User Story 4 - Secure User Isolation (Priority: P2)

**Goal**: Ensure all operations validate JWT tokens and enforce user data isolation

**Independent Test**: Attempting to access other users' data with different tokens is denied

**Why US4 before US1**: Security must be in place before exposing chat interface

### Implementation for User Story 4

- [X] T028 [US4] Implement JWT token validation in backend/src/middleware/auth.py
- [X] T029 [US4] Add user_id extraction from JWT in backend/src/utils/auth.py
- [X] T030 [US4] Add user_id filtering to TodoService queries in backend/src/services/todo_service.py
- [X] T031 [US4] Create authentication decorator for API endpoints in backend/src/utils/decorators.py
- [X] T032 [US4] Apply authentication to all todo endpoints in backend/src/api/todos.py
- [X] T033 [US4] Add user isolation tests for MCP tools in backend/src/api/mcp_tools.py
- [X] T034 [US4] Create error responses for unauthorized access in backend/src/utils/errors.py

**Checkpoint**: At this point, all operations should enforce proper user isolation

---

## Phase 5: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Users can manage todos through natural language chat interface

**Independent Test**: Send natural language commands and verify correct todo operations are performed

### Implementation for User Story 1

- [X] T035 [P] [US1] Install OpenAI SDK in backend/pyproject.toml
- [X] T036 [P] [US1] Install Axios for API calls in frontend/package.json
- [X] T037 [US1] Create AI agent service with OpenAI GPT-4 integration in backend/src/services/ai_agent_service.py
- [X] T038 [US1] Configure AI agent to discover MCP tools in backend/src/services/ai_agent_service.py
- [X] T039 [US1] Implement natural language intent parsing in backend/src/services/ai_agent_service.py
- [X] T040 [US1] Create chat endpoint to process messages in backend/src/api/chat.py
- [X] T041 [US1] Implement tool invocation logic in backend/src/services/ai_agent_service.py
- [X] T042 [US1] Add response formatting for chat in backend/src/services/ai_agent_service.py
- [X] T043 [P] [US1] Create ChatWindow component in frontend/src/components/ChatInterface/ChatWindow.tsx
- [X] T044 [P] [US1] Create Message component in frontend/src/components/ChatInterface/Message.tsx
- [X] T045 [P] [US1] Create InputArea component in frontend/src/components/ChatInterface/InputArea.tsx
- [X] T046 [US1] Create chat page with custom React components in frontend/src/app/chat/page.tsx
- [X] T047 [US1] Implement API service for chat in frontend/src/services/api.ts
- [X] T048 [US1] Add authentication headers to chat requests in frontend/src/services/auth.ts
- [X] T049 [US1] Integrate chat interface with backend API in frontend/src/app/chat/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can manage todos via natural language

---

## Phase 6: User Story 3 - Persistent Conversation History (Priority: P3)

**Goal**: Store and retrieve conversation history for context continuity across sessions

**Independent Test**: Simulate conversation, store history, retrieve it, and verify context is maintained

### Implementation for User Story 3

- [X] T050 [P] [US3] Create Conversation model in database/models/conversation.py
- [X] T051 [P] [US3] Create Message model in database/models/message.py
- [X] T052 [US3] Create database migration for conversations table in database/migrations/002_create_conversations.py
- [X] T053 [US3] Create database migration for messages table in database/migrations/003_create_messages.py
- [X] T054 [US3] Implement ConversationService in backend/src/services/conversation_service.py
- [X] T055 [US3] Add conversation creation logic in backend/src/services/conversation_service.py
- [X] T056 [US3] Add message storage logic in backend/src/services/conversation_service.py
- [X] T057 [US3] Add conversation history retrieval in backend/src/services/conversation_service.py
- [X] T058 [US3] Integrate conversation storage with chat endpoint in backend/src/api/chat.py
- [X] T059 [US3] Add conversation_id parameter to chat endpoint in backend/src/api/chat.py
- [X] T060 [US3] Create conversations list endpoint in backend/src/api/chat.py
- [X] T061 [US3] Create conversation messages endpoint in backend/src/api/chat.py
- [X] T062 [US3] Add conversation history UI in frontend/src/components/ChatInterface/ConversationHistory.tsx
- [X] T063 [US3] Integrate conversation history with chat page in frontend/src/app/chat/page.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T064 [P] Add comprehensive error handling across all endpoints in backend/src/api/
- [X] T065 [P] Add input validation for all API endpoints in backend/src/api/
- [X] T066 [P] Add logging for all MCP tool invocations in backend/src/api/mcp_tools.py
- [X] T067 [P] Add logging for chat interactions in backend/src/api/chat.py
- [X] T068 [P] Create TypeScript types for API responses in frontend/src/types/index.ts
- [X] T069 [P] Add loading states to chat interface in frontend/src/components/ChatInterface/
- [X] T070 [P] Add error display in chat interface in frontend/src/components/ChatInterface/
- [X] T071 [P] Optimize database queries with proper indexing in database/models/
- [X] T072 [P] Add rate limiting to chat endpoint in backend/src/middleware/rate_limit.py
- [X] T073 Create health check endpoint in backend/src/api/health.py
- [X] T074 Update quickstart.md with testing instructions in specs/003-ai-chatbot/quickstart.md
- [X] T075 Verify Phase II features still work after Phase III changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 2 (Phase 3)**: Depends on Foundational phase - MCP tools foundation
- **User Story 4 (Phase 4)**: Depends on Foundational phase - Security layer
- **User Story 1 (Phase 5)**: Depends on US2 and US4 completion - Uses MCP tools with security
- **User Story 3 (Phase 6)**: Depends on US1 completion - Enhances chat with history
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 2 (P2)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational - No dependencies on other stories
- **User Story 1 (P1)**: Depends on US2 (needs MCP tools) and US4 (needs security)
- **User Story 3 (P3)**: Depends on US1 (enhances existing chat functionality)

### Within Each User Story

- Models before services
- Services before API endpoints
- Backend before frontend integration
- Core implementation before enhancements

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- US2 and US4 can be worked on in parallel after Foundational phase
- Within each story, tasks marked [P] can run in parallel
- Frontend and backend tasks within a story can often run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch all MCP tool creation tasks together:
Task: "Create MCP tool for list-todos in backend/src/api/mcp_tools.py"
Task: "Create MCP tool for update-todo in backend/src/api/mcp_tools.py"
Task: "Create MCP tool for delete-todo in backend/src/api/mcp_tools.py"
Task: "Create MCP tool for toggle-todo-status in backend/src/api/mcp_tools.py"
```

---

## Implementation Strategy

### MVP First (User Stories 2, 4, and 1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 2 (MCP Tools)
4. Complete Phase 4: User Story 4 (Security)
5. Complete Phase 5: User Story 1 (Natural Language Chat)
6. **STOP and VALIDATE**: Test natural language task management independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 2 → Test MCP tools independently → Validate
3. Add User Story 4 → Test security independently → Validate
4. Add User Story 1 → Test chat interface independently → Deploy/Demo (MVP!)
5. Add User Story 3 → Test conversation history independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 2 (MCP Tools)
   - Developer B: User Story 4 (Security)
3. After US2 and US4 complete:
   - Developer A + B: User Story 1 (Chat Interface)
4. After US1 complete:
   - Developer C: User Story 3 (Conversation History)
5. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- US2 and US4 must complete before US1 can start (architectural dependencies)
- US3 enhances US1 but US1 can function without it
