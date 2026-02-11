# Tasks: Core Todo Operations

**Input**: Design documents from `/specs/001-core-features/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (required)

**Tests**: Not required - specification does not request automated tests (manual testing via quickstart.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/` at repository root
- Single file architecture: `src/todo_app.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src/ directory for source code in repository root
- [X] T002 Create initial src/todo_app.py file with module docstring and basic structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [P] Implement global data storage (task_store dict and next_task_id counter) in src/todo_app.py
- [X] T004 [P] Implement get_user_input(prompt, allow_empty) helper function in src/todo_app.py
- [X] T005 [P] Implement validate_title(title) helper function with trim, empty check, and 100-char truncation in src/todo_app.py
- [X] T006 [P] Implement validate_description(description) helper function with 500-char truncation in src/todo_app.py
- [X] T007 [P] Implement find_task(task_id) helper function with existence check and error handling in src/todo_app.py
- [X] T008 [P] Implement display_menu() function to show 6 menu options in src/todo_app.py
- [X] T009 Implement main() function with menu loop and option dispatch logic in src/todo_app.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Launch app, add task "Buy groceries" with description "Milk, eggs, bread", verify it appears with ID 1 and status "Pending"

### Implementation for User Story 1

- [X] T010 [US1] Implement add_task() function with prompts for title and description in src/todo_app.py
- [X] T011 [US1] Add title validation logic calling validate_title() with empty check and re-prompt in src/todo_app.py add_task()
- [X] T012 [US1] Add description validation logic calling validate_description() in src/todo_app.py add_task()
- [X] T013 [US1] Implement task creation logic: generate ID using next_task_id, create task dict, store in task_store in src/todo_app.py add_task()
- [X] T014 [US1] Add confirmation message display after successful task creation in src/todo_app.py add_task()
- [X] T015 [US1] Connect add_task() to main menu option 1 in src/todo_app.py main() function

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently via quickstart.md Scenarios 1-5

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Enable users to see all tasks with ID, title, description, and status

**Independent Test**: Add three tasks (varying statuses/descriptions), view all, verify all details displayed clearly sorted by ID

### Implementation for User Story 2

- [X] T016 [US2] Implement view_tasks() function skeleton in src/todo_app.py
- [X] T017 [US2] Add empty task store check displaying "No tasks found. Add your first task to get started!" in src/todo_app.py view_tasks()
- [X] T018 [US2] Implement task iteration logic with sorted IDs (ascending order) in src/todo_app.py view_tasks()
- [X] T019 [US2] Add formatted display for each task showing ID, title, description, status in src/todo_app.py view_tasks()
- [X] T020 [US2] Handle empty description display as "[No description]" in src/todo_app.py view_tasks()
- [X] T021 [US2] Connect view_tasks() to main menu option 2 in src/todo_app.py main() function

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (can add and view tasks) - testable via quickstart.md Scenarios 6-7

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to modify title and/or description of existing tasks by ID

**Independent Test**: Add task "Finsih report" / "By Friday", update to "Finish report" / "By Friday EOD", verify changes reflected

### Implementation for User Story 3

- [X] T022 [US3] Implement update_task() function skeleton with task ID prompt in src/todo_app.py
- [X] T023 [US3] Add task lookup using find_task() with error handling for invalid IDs in src/todo_app.py update_task()
- [X] T024 [US3] Implement title update prompt with validation (validate_title, empty check, re-prompt) in src/todo_app.py update_task()
- [X] T025 [US3] Implement description update prompt with validation (validate_description) in src/todo_app.py update_task()
- [X] T026 [US3] Update task_store with new title and/or description preserving ID and status in src/todo_app.py update_task()
- [X] T027 [US3] Add confirmation message after successful update in src/todo_app.py update_task()
- [X] T028 [US3] Connect update_task() to main menu option 3 in src/todo_app.py main() function

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently - testable via quickstart.md Scenarios 8-10

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Enable users to remove tasks by ID with confirmation

**Independent Test**: Add three tasks, delete middle one (ID 2), verify it's gone and IDs 1,3 remain

### Implementation for User Story 4

- [X] T029 [US4] Implement delete_task() function skeleton with task ID prompt in src/todo_app.py
- [X] T030 [US4] Add task lookup using find_task() with error handling for invalid IDs in src/todo_app.py delete_task()
- [X] T031 [US4] Implement task deletion logic removing task from task_store using del in src/todo_app.py delete_task()
- [X] T032 [US4] Add confirmation message "Task ID {id} deleted successfully" in src/todo_app.py delete_task()
- [X] T033 [US4] Connect delete_task() to main menu option 4 in src/todo_app.py main() function

**Checkpoint**: User Stories 1-4 should all work independently - testable via quickstart.md Scenarios 11-13

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: Enable users to toggle task status between "Pending" and "Completed"

**Independent Test**: Add task, mark complete (verify "Completed"), mark incomplete (verify "Pending")

### Implementation for User Story 5

- [X] T034 [US5] Implement toggle_task_status() function skeleton with task ID prompt in src/todo_app.py
- [X] T035 [US5] Add task lookup using find_task() with error handling for invalid IDs in src/todo_app.py toggle_task_status()
- [X] T036 [US5] Implement status toggle logic: if "Pending" set "Completed", if "Completed" set "Pending" in src/todo_app.py toggle_task_status()
- [X] T037 [US5] Add confirmation message "Task ID {id} marked as {new_status}" in src/todo_app.py toggle_task_status()
- [X] T038 [US5] Connect toggle_task_status() to main menu option 5 in src/todo_app.py main() function

**Checkpoint**: All user stories (1-5) should now be independently functional - testable via quickstart.md Scenarios 14-17

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories and edge case handling

- [X] T039 [P] Add invalid menu choice handling with error message "Invalid choice. Please try again." in src/todo_app.py main()
- [X] T040 [P] Add exit option (menu option 6) to break main loop and terminate application in src/todo_app.py main()
- [X] T041 [P] Add PEP 8 formatting review: check 4-space indentation, naming conventions, line length <100 chars in src/todo_app.py
- [X] T042 [P] Add module-level docstring explaining application purpose and usage at top of src/todo_app.py
- [X] T043 [P] Add docstrings for all functions (11 total) using Google or NumPy style in src/todo_app.py
- [X] T044 Run full manual test suite from quickstart.md (all 20 scenarios) and document results

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (though naturally complements US1)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Independently testable

**Key Insight**: After Foundational phase, ALL 5 user stories are truly independent and can be implemented in any order or in parallel!

### Within Each User Story

- Tasks within a user story must run sequentially (T010 → T011 → T012 → ... → T015 for US1)
- Exception: Connecting to menu (last task in each story) requires the story's main function to be complete

### Parallel Opportunities

- **Setup (Phase 1)**: T001 and T002 could run in parallel if using different processes
- **Foundational (Phase 2)**: T003-T008 marked [P] can all run in parallel (different functions, no dependencies)
- **User Stories (Phase 3-7)**: Once Foundational completes, all 5 user stories can be worked on in parallel by different developers
- **Polish (Phase 8)**: T039-T043 marked [P] can run in parallel (independent concerns)

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational helper functions together:
Task: "Implement global data storage in src/todo_app.py"
Task: "Implement get_user_input() helper in src/todo_app.py"
Task: "Implement validate_title() helper in src/todo_app.py"
Task: "Implement validate_description() helper in src/todo_app.py"
Task: "Implement find_task() helper in src/todo_app.py"
Task: "Implement display_menu() function in src/todo_app.py"

# Then sequentially:
Task: "Implement main() function with menu loop" (depends on display_menu being done)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T009) - CRITICAL foundation
3. Complete Phase 3: User Story 1 (T010-T015)
4. **STOP and VALIDATE**: Test User Story 1 independently via quickstart.md Scenarios 1-5
5. Demo MVP - users can add tasks!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T010-T015) → Test independently → Demo (MVP - can add tasks!)
3. Add User Story 2 (T016-T021) → Test independently → Demo (can add AND view tasks!)
4. Add User Story 3 (T022-T028) → Test independently → Demo (can add, view, AND edit tasks!)
5. Add User Story 4 (T029-T033) → Test independently → Demo (add/view/edit/delete)
6. Add User Story 5 (T034-T038) → Test independently → Demo (full CRUD + status)
7. Add Polish (T039-T044) → Full manual testing → Production ready!

Each increment adds value without breaking previous stories.

### Sequential Strategy (Single Developer)

Follow priority order strictly:

1. Setup (Phase 1)
2. Foundational (Phase 2) - MUST complete fully
3. User Story 1/P1 (Phase 3) - MVP
4. User Story 2/P2 (Phase 4)
5. User Story 3/P3 (Phase 5)
6. User Story 4/P4 (Phase 6)
7. User Story 5/P5 (Phase 7)
8. Polish (Phase 8)
9. Full manual testing

### Parallel Team Strategy

With multiple developers:

1. **Everyone**: Setup + Foundational together (T001-T009)
2. **Once Foundational done, split work**:
   - Developer A: User Story 1 (T010-T015)
   - Developer B: User Story 2 (T016-T021)
   - Developer C: User Story 3 (T022-T028)
   - Developer D: User Story 4 (T029-T033)
   - Developer E: User Story 5 (T034-T038)
3. Stories complete and integrate independently (single file, but different functions)
4. **Everyone**: Polish together (T039-T044)

---

## Notes

- [P] tasks = different functions/concerns, no dependencies (can parallelize)
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable via quickstart.md
- Single-file architecture means no import/module issues
- Foundational phase is CRITICAL - all helper functions must work before any user story
- Commit after each user story phase for clean history
- Stop at any checkpoint to validate story independently
- Manual testing required - no automated tests per constitution and spec

---

## Task Count Summary

- **Phase 1 (Setup)**: 2 tasks
- **Phase 2 (Foundational)**: 7 tasks (6 parallelizable)
- **Phase 3 (US1 - P1)**: 6 tasks
- **Phase 4 (US2 - P2)**: 6 tasks
- **Phase 5 (US3 - P3)**: 7 tasks
- **Phase 6 (US4 - P4)**: 5 tasks
- **Phase 7 (US5 - P5)**: 5 tasks
- **Phase 8 (Polish)**: 6 tasks (5 parallelizable)

**Total**: 44 tasks

**Parallel Opportunities**: 11 tasks marked [P] (25% of tasks can run in parallel)

**Critical Path**: Setup (2) → Foundational (7, sequential after parallel work) → Any US (5-7) → Polish (6) ≈ 20-24 tasks on critical path
