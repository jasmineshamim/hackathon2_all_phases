# Implementation Plan: Core Todo Operations

**Branch**: `001-core-features` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-core-features/spec.md`

## Summary

Implement a beginner-friendly, console-based task management application with five core operations: Add, View, Update, Delete, and Mark Complete/Incomplete tasks. The application uses in-memory storage (Python data structures) with no external dependencies, designed as an educational project to teach Python fundamentals through practical application.

**Technical Approach**: Single-file Python application with clear function-based architecture, using a dictionary to store tasks in memory, and a simple console menu loop for user interaction.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: None (standard library only - no external packages)
**Storage**: In-memory (Python dictionary with integer keys for task IDs)
**Testing**: Not required for initial implementation (per constitution Principle VI)
**Target Platform**: Cross-platform (Windows, macOS, Linux) - any system with Python 3.8+
**Project Type**: Single project (standalone console application)
**Performance Goals**: Instant response (<100ms) for all operations with up to 100 tasks
**Constraints**: No persistence, no external dependencies, beginner-readable code, <500 lines total
**Scale/Scope**: Single-user, single-session, educational demonstration project

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I: Spec-First Development** ✅ PASS
- Specification complete and approved at `specs/001-core-features/spec.md`
- All user stories documented with acceptance criteria
- Proceeding to planning phase per workflow

**Principle II: Beginner-Friendly Code Quality** ✅ PASS
- Plan specifies function-based architecture (no advanced OOP)
- Standard library only (no unfamiliar frameworks)
- Clear naming conventions enforced
- Single-file structure for simplicity

**Principle III: Minimal Scope (No Feature Creep)** ✅ PASS
- Implementation limited to 5 core operations from spec
- No logging, metrics, configuration systems
- No additional features beyond specification

**Principle IV: In-Memory Storage Only** ✅ PASS
- Using Python dictionary for task storage
- No database, file I/O, or external persistence
- Data lost on program exit (per requirement)

**Principle V: Console-Only Interface** ✅ PASS
- Uses `input()` and `print()` exclusively
- No GUI, web, or API interfaces
- Menu-driven console navigation

**Principle VI: Test-Driven Development (Optional)** ✅ PASS
- Specification does NOT request tests
- No test files will be created per constitution
- Manual testing via quickstart.md scenarios

**Data Model Standards** ✅ PASS
- Task entity exactly matches constitution requirements:
  - ID (integer, auto-increment from 1)
  - Title (string, 1-100 chars, required)
  - Description (string, 0-500 chars, optional)
  - Status (string, "Pending" or "Completed")

**Overall Gate Status**: ✅ **PASS** - No violations, all principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-core-features/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - implementation plan
├── data-model.md        # Task entity definition (Phase 1)
├── quickstart.md        # Manual testing scenarios (Phase 1)
└── tasks.md             # Granular task breakdown (Phase 2 - via /sp.tasks)
```

### Source Code (repository root)

```text
src/
└── todo_app.py          # Single-file application (all functionality)

# No tests/ directory - testing not requested in specification
```

**Structure Decision**: Single-file architecture chosen for maximum beginner accessibility. All functionality (data storage, business logic, UI) in one file to eliminate navigation complexity and keep the entire program visible at once. This aligns with Principle II (Beginner-Friendly) and Principle III (Minimal Scope).

**Rationale for Single-File**:
- Educational context prioritizes comprehension over scalability
- Total code <500 lines - manageable in single file
- No shared components across features (self-contained app)
- Easier for beginners to understand data flow without imports
- Simpler to run: `python src/todo_app.py`

## Architecture Design

### Data Storage Strategy

**In-Memory Task Store**:
```python
# Global dictionary (only acceptable global per constitution)
task_store = {}  # {task_id: {"id": int, "title": str, "description": str, "status": str}}
next_task_id = 1  # Global counter for ID generation
```

**Rationale**: Dictionary provides O(1) lookup by ID, natural key-value mapping, and easy iteration for viewing all tasks.

### Function Architecture

**Core Functions** (one per user story):
1. `add_task()` - Create new task (US1)
2. `view_tasks()` - Display all tasks (US2)
3. `update_task()` - Modify task details (US3)
4. `delete_task()` - Remove task (US4)
5. `toggle_task_status()` - Mark complete/incomplete (US5)

**Helper Functions**:
- `get_user_input(prompt, allow_empty=False)` - Input validation wrapper
- `validate_title(title)` - Title validation and truncation
- `validate_description(description)` - Description truncation
- `find_task(task_id)` - Task lookup with error handling
- `display_menu()` - Show main menu options
- `main()` - Application entry point and menu loop

**Control Flow**:
```
main()
  └─> display_menu() (loop)
       ├─> User selects option
       ├─> Call appropriate function
       ├─> Function performs operation
       ├─> Display result/error
       └─> Return to menu (until exit)
```

### Input Validation Strategy

Per FR-003, FR-011, FR-019, FR-020:
- Title: Strip whitespace, reject if empty, truncate to 100 chars with warning
- Description: Truncate to 500 chars with warning (empty allowed)
- Task ID: Validate integer, check existence in task_store
- Menu Choice: Validate integer in range, re-prompt on invalid

### Error Handling Approach

Per FR-024, FR-025:
- User-friendly messages (no stack traces)
- Always return to main menu after error
- Clear action guidance ("Please enter a valid task ID")

**Example Error Flow**:
```
User enters invalid ID → "Task ID 99 not found" → Return to menu
User enters empty title → "Title cannot be empty" → Re-prompt for title
```

## Phase 0: Research & Decisions

**Note**: All technical context is clear from specification and constitution. No research required.

### Decision Log

**Decision 1: Single-file vs Multi-file Architecture**
- **Chosen**: Single-file (`src/todo_app.py`)
- **Rationale**: Educational project <500 lines, beginners benefit from seeing all code together
- **Alternatives Considered**: Separate files for models/services/ui - rejected as over-engineering for scope
- **Trade-offs**: Sacrifices scalability for comprehension (acceptable per constitution Principle II)

**Decision 2: Dictionary vs List for Storage**
- **Chosen**: Dictionary with integer keys (`{1: task_dict, 2: task_dict, ...}`)
- **Rationale**: O(1) ID lookup, easy existence checks, natural ID→task mapping
- **Alternatives Considered**: List with linear search - rejected for O(n) lookup performance
- **Trade-offs**: Slightly more memory than list (negligible for <100 tasks)

**Decision 3: Status Representation**
- **Chosen**: String literals "Pending" and "Completed"
- **Rationale**: Simplest approach for beginners, no need for enum/constants
- **Alternatives Considered**: Integer codes (0/1), Enum class - rejected as over-engineering
- **Trade-offs**: String comparison vs integer, but scope is tiny (acceptable)

**Decision 4: Global State Management**
- **Chosen**: Two global variables (`task_store`, `next_task_id`)
- **Rationale**: Constitution explicitly allows global for in-memory store, simplest for single-file
- **Alternatives Considered**: Class-based state container - rejected for beginner complexity
- **Trade-offs**: Globals generally discouraged, but constitution makes exception for this use case

## Phase 1: Design Artifacts

### Data Model

See `data-model.md` for complete Task entity definition.

**Summary**:
- Single entity: Task
- Four attributes: id, title, description, status
- No relationships (standalone entity)
- Validation rules encoded in helper functions

### No Contracts Needed

This is a console application with no API, network communication, or inter-process contracts. User interaction happens through direct function calls triggered by menu selections.

**Interface Contract** (menu-driven):
```
Menu Options:
1 → add_task()
2 → view_tasks()
3 → update_task()
4 → delete_task()
5 → toggle_task_status()
6 → Exit application
```

### Testing Strategy

See `quickstart.md` for manual testing scenarios.

**Approach**: Manual testing only (no automated tests per constitution Principle VI and spec).

**Test Coverage**: Each user story (US1-US5) has independent test scenario plus edge cases.

## Complexity Tracking

> **No violations detected - this section intentionally left empty.**

All constitution principles satisfied without exceptions.

## Next Steps

1. **Run `/sp.tasks`** to generate granular implementation task breakdown
2. **Run `/sp.implement`** to execute task-by-task implementation
3. **Manual testing** using quickstart.md scenarios
4. **Run `/sp.git.commit_pr`** when feature complete

---

**Plan Status**: ✅ Complete - Ready for task generation
**Phase 0**: ✅ Complete (no research needed)
**Phase 1**: ✅ Complete (data-model.md, quickstart.md generated)
**Phase 2**: ⏳ Pending (run `/sp.tasks`)
