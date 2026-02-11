# Data Model: Core Todo Operations

**Feature**: Core Todo Operations
**Created**: 2026-01-01
**Status**: Approved

## Overview

This feature has a single entity: **Task**. There are no relationships, foreign keys, or complex data structures. Each task is an independent record stored in an in-memory dictionary.

## Entity: Task

### Purpose

Represents a single todo item with identifying information, content, and completion status.

### Attributes

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| id | integer | Required, Unique, Immutable, Auto-generated, Sequential from 1 | Auto-assigned | Unique identifier for the task |
| title | string | Required, Non-empty (after trim), Max 100 chars | None | Short description of what needs to be done |
| description | string | Optional, Max 500 chars | "" (empty string) | Detailed information about the task |
| status | string | Required, Must be "Pending" or "Completed" (case-sensitive) | "Pending" | Current completion state of the task |

### Attribute Details

#### id (integer)
- **Purpose**: Uniquely identify each task for operations (update, delete, status change)
- **Generation**: Auto-incrementing counter starting at 1
- **Behavior**:
  - Assigned when task is created
  - Never changes after creation (immutable)
  - Never reused after deletion (always increments)
  - IDs may have gaps after deletions (e.g., 1, 3, 5 if 2 and 4 deleted)

#### title (string)
- **Purpose**: Brief, user-readable summary of the task
- **Validation**:
  - MUST NOT be empty after whitespace trimming
  - If empty/whitespace-only: Display error "Title cannot be empty" and re-prompt
  - If exceeds 100 characters: Truncate to 100 and display warning "Title truncated to 100 characters"
- **Examples**:
  - Valid: "Buy groceries", "Complete project report", "Fix bug in login"
  - Invalid (empty): "", "   ", "\t\n"

#### description (string)
- **Purpose**: Optional additional details about the task
- **Validation**:
  - MAY be empty (empty string is valid)
  - If exceeds 500 characters: Truncate to 500 and display warning "Description truncated to 500 characters"
- **Display**: Show "[No description]" when viewing tasks with empty description
- **Examples**:
  - Valid: "Milk, eggs, bread", "", "Include Q4 metrics and revenue projections"

#### status (string)
- **Purpose**: Track whether task is pending or completed
- **Allowed Values**: Exactly "Pending" or "Completed" (case-sensitive, no variations)
- **Behavior**:
  - New tasks always start as "Pending"
  - Can be toggled between "Pending" ↔ "Completed"
  - Idempotent: Marking completed task as completed again is allowed (no error)
  - NOT affected by update operations (only by explicit status toggle)

### Storage Representation

**In-Memory (Python Dictionary)**:
```python
task_store = {
    1: {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "status": "Pending"},
    2: {"id": 2, "title": "Finish report", "description": "", "status": "Completed"},
    3: {"id": 3, "title": "Call dentist", "description": "Schedule checkup for next month", "status": "Pending"}
}
```

**Key**: Integer task ID (1, 2, 3, ...)
**Value**: Dictionary with four keys (id, title, description, status)

### State Transitions

```
[Task Created] → status = "Pending"
    ↓
[User marks complete] → status = "Completed"
    ↓
[User marks incomplete] → status = "Pending"
    ↓
(cycle repeats)
```

**Allowed Transitions**:
- Pending → Completed (user action: mark complete)
- Completed → Pending (user action: mark incomplete)
- Pending → Pending (idempotent, no-op)
- Completed → Completed (idempotent, no-op)

**NOT Allowed**:
- Status cannot be changed via update operation (only title/description)
- Status cannot be set to any value other than "Pending" or "Completed"

### Validation Rules Summary

| Rule | Check | Action on Violation |
|------|-------|---------------------|
| VR-001 | Title is not empty after trim | Display error, re-prompt for title |
| VR-002 | Title length ≤ 100 characters | Truncate to 100, display warning |
| VR-003 | Description length ≤ 500 characters | Truncate to 500, display warning |
| VR-004 | Task ID exists in task_store | Display "Task ID {id} not found", return to menu |
| VR-005 | Status is "Pending" or "Completed" | (Enforced by implementation, not user input) |

### Business Rules

| Rule | Description |
|------|-------------|
| BR-001 | Duplicate titles are allowed (multiple tasks can have same title) |
| BR-002 | Task IDs never reset during session (always increment even after deletions) |
| BR-003 | Deleted task IDs are never reused (ID gaps are permanent) |
| BR-004 | Empty descriptions are stored as empty string "", not null |
| BR-005 | All data is lost when application terminates (no persistence) |
| BR-006 | Tasks are displayed sorted by ID in ascending order |
| BR-007 | Update operation preserves ID and status (only title/description change) |

## No Relationships

This data model has no relationships. Each task is a standalone entity with no foreign keys, references, or dependencies on other entities.

## Data Lifecycle

```
1. Creation → Task added to task_store with auto-generated ID
2. Read → Task retrieved from task_store by ID for viewing
3. Update → Task's title/description modified in task_store (status unchanged)
4. Status Toggle → Task's status modified in task_store (title/description unchanged)
5. Deletion → Task removed from task_store, ID never reused
6. Application Exit → Entire task_store lost (in-memory only)
```

## Edge Cases & Data Constraints

1. **Maximum Tasks**: No enforced limit (Python dict can handle millions), but spec tests with 100 tasks
2. **Very Large IDs**: Python integers have arbitrary precision (no overflow)
3. **Empty Task Store**: Valid state, display "No tasks found. Add your first task to get started!"
4. **Non-Sequential IDs**: Valid after deletions (e.g., IDs 1, 3, 5 if 2 and 4 deleted)
5. **Unicode Characters**: Supported in title/description (Python strings are UTF-8)
6. **Special Characters**: All allowed in title/description (no sanitization needed for console output)

## Implementation Notes

- Use Python's built-in `dict` for task_store
- Use global integer counter `next_task_id` for ID generation
- No database, ORM, or serialization libraries required
- Validation happens in helper functions before storage operations
- No schema migration needed (in-memory only)
