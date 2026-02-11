# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/app/`, `frontend/components/`
- Paths follow monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Verify existing Phase II structure (backend/, frontend/, database/)
- [x] T002 Install backend dependencies: fastapi, openai, mcp-sdk, sqlmodel in backend/requirements.txt
- [x] T003 [P] Install frontend dependencies: @openai/chatkit in frontend/package.json
- [x] T004 [P] Configure environment variables for OpenAI API key in backend/.env
- [x] T005 [P] Configure OpenAI ChatKit domain key in frontend/.env.local

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [x] T006 Create Conversation SQLModel in backend/src/models/conversation.py
- [x] T007 [P] Create Message SQLModel in backend/src/models/message.py
- [x] T008 Create Alembic migration script for conversations and messages tables in backend/src/db/migrations/versions/003_add_conversation_tables.py
- [x] T009 Run database migrations to create conversations and messages tables

### MCP Server Foundation

- [x] T010 Create MCP server initialization in backend/src/mcp/server.py
- [x] T011 [P] Create MCP tool schemas in backend/src/mcp/schemas.py
- [x] T012 [P] Create add_task MCP tool in backend/src/mcp/tools/add_task.py
- [x] T013 [P] Create list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py
- [x] T014 [P] Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py
- [x] T015 [P] Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py
- [x] T016 [P] Create update_task MCP tool in backend/src/mcp/tools/update_task.py
- [x] T017 Register all MCP tools with MCP server in backend/src/mcp/server.py

### OpenAI Agents SDK Setup

- [x] T018 Create agent system prompts in backend/src/agents/prompts.py
- [x] T019 Create chat agent initialization in backend/src/agents/chat_agent.py
- [x] T020 Configure agent with MCP tools in backend/src/agents/chat_agent.py

### Service Layer Foundation

- [x] T021 Create ConversationService in backend/src/services/conversation_service.py
- [x] T022 [P] Create MessageService in backend/src/services/message_service.py

### API Infrastructure

- [x] T023 Create chat endpoint route file in backend/src/api/routes/chat.py
- [x] T024 Register chat route with FastAPI app in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing natural language commands like "Add a task to buy groceries"

**Independent Test**: User types "Add a task to buy groceries" and system creates task with title "Buy groceries", confirming in chat

### Implementation for User Story 1

- [x] T025 [US1] Implement conversation creation logic in backend/src/services/conversation_service.py
- [x] T026 [US1] Implement message storage logic in backend/src/services/message_service.py
- [x] T027 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/routes/chat.py
- [x] T028 [US1] Add JWT token validation in chat endpoint in backend/src/api/routes/chat.py
- [x] T029 [US1] Implement conversation history retrieval in backend/src/services/conversation_service.py
- [x] T030 [US1] Implement message array construction for agent in backend/src/agents/chat_agent.py
- [x] T031 [US1] Integrate agent invocation in chat endpoint in backend/src/api/routes/chat.py
- [x] T032 [US1] Add response formatting and tool_calls in chat endpoint in backend/src/api/routes/chat.py
- [x] T033 [US1] Create chat page component in frontend/app/chat/page.tsx
- [x] T034 [US1] Implement ChatInterface component (custom implementation) in frontend/components/chat/ChatInterface.tsx
- [x] T035 [US1] Create chat API client in frontend/lib/chat-client.ts
- [x] T036 [US1] Add chat link to navigation in frontend/components/Navbar.tsx
- [x] T037 [US1] Configure chat authentication (using existing JWT from api-client)
- [ ] T038 [US1] Test task creation via natural language: "Add a task to buy groceries"

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks through conversation

---

## Phase 4: User Story 2 - View and List Tasks (Priority: P1)

**Goal**: Users can view their tasks through natural language queries like "Show me my tasks" or "What's pending?"

**Independent Test**: User types "Show me my tasks" and receives formatted list of their tasks with status

### Implementation for User Story 2

- [ ] T039 [US2] Verify list_tasks MCP tool filters by user_id in backend/src/mcp/tools/list_tasks.py
- [ ] T040 [US2] Verify list_tasks MCP tool supports status filtering (all/pending/completed) in backend/src/mcp/tools/list_tasks.py
- [ ] T041 [US2] Update agent prompts to handle list queries in backend/src/agents/prompts.py
- [ ] T042 [US2] Add task list formatting in agent responses in backend/src/agents/chat_agent.py
- [ ] T043 [US2] Test task listing via natural language: "Show me all my tasks"
- [ ] T044 [US2] Test filtered listing: "What's pending?"
- [ ] T045 [US2] Test empty list handling: "Show me my tasks" with no tasks

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P1)

**Goal**: Users can mark tasks as complete through natural language like "Mark task 3 as complete" or "I finished the groceries task"

**Independent Test**: User types "Mark task 3 as complete" and system updates task status, confirming in chat

### Implementation for User Story 3

- [ ] T046 [US3] Verify complete_task MCP tool updates task status in backend/src/mcp/tools/complete_task.py
- [ ] T047 [US3] Add task completion confirmation messages in agent prompts in backend/src/agents/prompts.py
- [ ] T048 [US3] Handle task not found errors in complete_task tool in backend/src/mcp/tools/complete_task.py
- [ ] T049 [US3] Handle already completed tasks in complete_task tool in backend/src/mcp/tools/complete_task.py
- [ ] T050 [US3] Test task completion by ID: "Mark task 3 as complete"
- [ ] T051 [US3] Test task completion by title: "I finished buying groceries"
- [ ] T052 [US3] Test error handling: "Mark task 999 as complete" (non-existent task)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update and Delete Tasks (Priority: P2)

**Goal**: Users can update or delete tasks through conversation like "Change task 1 to 'Call mom tonight'" or "Delete the meeting task"

**Independent Test**: User types "Change task 1 to 'Call mom tonight'" and system updates task title, confirming in chat

### Implementation for User Story 4

- [ ] T053 [US4] Verify update_task MCP tool updates title and/or description in backend/src/mcp/tools/update_task.py
- [ ] T054 [US4] Verify delete_task MCP tool removes task in backend/src/mcp/tools/delete_task.py
- [ ] T055 [US4] Add update confirmation messages in agent prompts in backend/src/agents/prompts.py
- [ ] T056 [US4] Add delete confirmation messages in agent prompts in backend/src/agents/prompts.py
- [ ] T057 [US4] Handle task not found errors in update_task tool in backend/src/mcp/tools/update_task.py
- [ ] T058 [US4] Handle task not found errors in delete_task tool in backend/src/mcp/tools/delete_task.py
- [ ] T059 [US4] Test task update: "Change task 1 to 'Call mom tonight'"
- [ ] T060 [US4] Test task deletion: "Delete task 2"
- [ ] T061 [US4] Test error handling for non-existent tasks

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Conversation History and Context (Priority: P2)

**Goal**: Users' conversation history persists across sessions and can be resumed

**Independent Test**: User closes browser, returns later, and sees previous conversation history with chatbot

### Implementation for User Story 5

- [ ] T062 [US5] Implement conversation history loading on chat page mount in frontend/app/chat/page.tsx
- [ ] T063 [US5] Create MessageList component to display history in frontend/components/chat/MessageList.tsx
- [ ] T064 [US5] Add conversation_id persistence in chat client in frontend/lib/chat-client.ts
- [ ] T065 [US5] Implement conversation history pagination (last 50 messages) in backend/src/services/conversation_service.py
- [ ] T066 [US5] Add conversation updated_at timestamp update in backend/src/services/conversation_service.py
- [ ] T067 [US5] Test conversation persistence: send messages, close browser, reopen
- [ ] T068 [US5] Test conversation history display on page load
- [ ] T069 [US5] Test context maintenance: "What did I just add?" references previous messages

**Checkpoint**: At this point, User Stories 1-5 should all work independently with full conversation persistence

---

## Phase 8: User Story 6 - Error Handling and Guidance (Priority: P3)

**Goal**: Users receive helpful error messages and guidance when chatbot doesn't understand requests

**Independent Test**: User types unclear command and receives helpful guidance on how to phrase requests correctly

### Implementation for User Story 6

- [ ] T070 [US6] Add error handling for unclear intents in backend/src/agents/chat_agent.py
- [ ] T071 [US6] Create help command handler in agent prompts in backend/src/agents/prompts.py
- [ ] T072 [US6] Add example commands in help responses in backend/src/agents/prompts.py
- [ ] T073 [US6] Implement graceful error messages for OpenAI API failures in backend/src/api/routes/chat.py
- [ ] T074 [US6] Implement graceful error messages for database failures in backend/src/api/routes/chat.py
- [ ] T075 [US6] Add user-friendly error display in ChatInterface component in frontend/components/chat/ChatInterface.tsx
- [ ] T076 [US6] Test unclear command: "groceries" (ambiguous intent)
- [ ] T077 [US6] Test help command: "help" or "what can you do?"
- [ ] T078 [US6] Test error scenarios: database connection failure, OpenAI API timeout

**Checkpoint**: All user stories should now be independently functional with comprehensive error handling

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Performance Optimization

- [ ] T079 [P] Add database indexes verification in backend/src/db/migrations/
- [ ] T080 [P] Implement connection pooling configuration in backend/src/db/database.py
- [ ] T081 [P] Add conversation history pagination UI in frontend/components/chat/MessageList.tsx

### Security Hardening

- [ ] T082 [P] Add rate limiting on chat endpoint in backend/src/api/routes/chat.py
- [ ] T083 [P] Add input validation for message length (max 2000 chars) in backend/src/api/routes/chat.py
- [ ] T084 [P] Verify user_id matches JWT token in chat endpoint in backend/src/api/routes/chat.py

### User Experience

- [ ] T085 [P] Add loading states in ChatInterface component in frontend/components/chat/ChatInterface.tsx
- [ ] T086 [P] Add optimistic UI updates in chat client in frontend/lib/chat-client.ts
- [ ] T087 [P] Add message timestamps display in MessageList component in frontend/components/chat/MessageList.tsx

### Documentation

- [ ] T088 [P] Update README.md with Phase III setup instructions
- [ ] T089 [P] Document MCP tools in backend/src/mcp/README.md
- [ ] T090 [P] Document agent configuration in backend/src/agents/README.md

### Testing & Validation

- [ ] T091 Run quickstart.md validation for all user stories
- [ ] T092 Verify all 6 user stories work independently
- [ ] T093 Test conversation flow end-to-end: create → list → complete → update → delete
- [ ] T094 Test concurrent chat sessions (multiple users)
- [ ] T095 Test conversation persistence after server restart

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent (uses existing list_tasks tool)
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Independent (uses existing complete_task tool)
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Independent (uses existing update/delete tools)
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Independent (adds history display)
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Independent (adds error handling)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T003, T004, T005 can run in parallel
- **Foundational Phase**:
  - T007 (Message model) parallel with T006 (Conversation model)
  - T012-T016 (all MCP tools) can run in parallel
  - T021-T022 (services) can run in parallel
- **After Foundational**: All user stories (Phase 3-8) can start in parallel if team capacity allows
- **Polish Phase**: T079-T090 (most polish tasks) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all MCP tool implementations together:
Task: "Create add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task: "Create list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py"
Task: "Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py"
Task: "Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py"
Task: "Create update_task MCP tool in backend/src/mcp/tools/update_task.py"

# Launch service layer together:
Task: "Create ConversationService in backend/src/services/conversation_service.py"
Task: "Create MessageService in backend/src/services/message_service.py"
```

## Parallel Example: User Stories (with team)

```bash
# After Foundational phase completes, launch all P1 stories in parallel:
Developer A: Phase 3 - User Story 1 (Natural Language Task Creation)
Developer B: Phase 4 - User Story 2 (View and List Tasks)
Developer C: Phase 5 - User Story 3 (Mark Tasks Complete)

# Then P2 stories:
Developer A: Phase 6 - User Story 4 (Update and Delete Tasks)
Developer B: Phase 7 - User Story 5 (Conversation History)

# Finally P3:
Developer A: Phase 8 - User Story 6 (Error Handling)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T024) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T025-T038)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - Users can now create tasks via chat!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - task creation!)
3. Add User Story 2 → Test independently → Deploy/Demo (+ task viewing!)
4. Add User Story 3 → Test independently → Deploy/Demo (+ task completion!)
5. Add User Story 4 → Test independently → Deploy/Demo (+ update/delete!)
6. Add User Story 5 → Test independently → Deploy/Demo (+ conversation history!)
7. Add User Story 6 → Test independently → Deploy/Demo (+ error handling!)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T024)
2. Once Foundational is done:
   - Developer A: User Story 1 (T025-T038)
   - Developer B: User Story 2 (T039-T045)
   - Developer C: User Story 3 (T046-T052)
3. Then continue with P2 stories:
   - Developer A: User Story 4 (T053-T061)
   - Developer B: User Story 5 (T062-T069)
4. Finally P3:
   - Developer A: User Story 6 (T070-T078)
5. All developers: Polish phase (T079-T095)

---

## Task Summary

**Total Tasks**: 95 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 19 tasks (CRITICAL - blocks all stories)
- Phase 3 (US1 - Task Creation): 14 tasks
- Phase 4 (US2 - View Tasks): 7 tasks
- Phase 5 (US3 - Complete Tasks): 7 tasks
- Phase 6 (US4 - Update/Delete): 9 tasks
- Phase 7 (US5 - History): 8 tasks
- Phase 8 (US6 - Error Handling): 9 tasks
- Phase 9 (Polish): 17 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**MVP Scope** (Recommended first delivery):
- Phase 1: Setup (5 tasks)
- Phase 2: Foundational (19 tasks)
- Phase 3: User Story 1 only (14 tasks)
- **Total MVP**: 38 tasks

**Independent Test Criteria**:
- US1: User can create tasks via "Add a task to..."
- US2: User can view tasks via "Show me my tasks"
- US3: User can complete tasks via "Mark task X as complete"
- US4: User can update/delete tasks via "Change task..." or "Delete task..."
- US5: Conversation history persists across sessions
- US6: Helpful error messages for unclear commands

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Foundational phase (Phase 2) is CRITICAL - must complete before any user story work
- All MCP tools are created in Foundational phase and reused by user stories
- Tests are NOT included as they were not explicitly requested in the specification
