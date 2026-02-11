# Cross-Phase User Journeys

This document captures user journeys that span across multiple phases of the Evolution of Todo application.

## The 5 Core Features (All Phases)

These features must be available in every phase, though the interface changes:

### 1. Add Task
**User Story**: As a user, I can create a new task with a title and optional description.

**Phase 1 (Console)**: User types task details at command prompt.
**Phase 2 (Web)**: User fills out web form and clicks "Add Task".
**Phase 3 (Chatbot)**: User says "Add a task to buy groceries" in chat.

### 2. View Tasks
**User Story**: As a user, I can see all my tasks with their status.

**Phase 1 (Console)**: User selects "View Tasks" from menu.
**Phase 2 (Web)**: User sees task list on dashboard.
**Phase 3 (Chatbot)**: User asks "Show me all my tasks" in chat.

### 3. Update Task
**User Story**: As a user, I can modify an existing task's title or description.

**Phase 1 (Console)**: User selects task by ID and provides new details.
**Phase 2 (Web)**: User clicks edit button on task.
**Phase 3 (Chatbot)**: User says "Change task 1 to buy fruits" in chat.

### 4. Delete Task
**User Story**: As a user, I can remove a task from my list.

**Phase 1 (Console)**: User selects task by ID and confirms deletion.
**Phase 2 (Web)**: User clicks delete button on task.
**Phase 3 (Chatbot)**: User says "Delete the meeting task" in chat.

### 5. Mark Complete/Incomplete
**User Story**: As a user, I can toggle a task's completion status.

**Phase 1 (Console)**: User selects task by ID to toggle status.
**Phase 2 (Web)**: User clicks checkbox on task.
**Phase 3 (Chatbot)**: User says "Mark task 3 as complete" in chat.

## Common Commands (Phase 3)

The chatbot should understand these natural language patterns:

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to call mom" | Call `update_task` with new title |
| "What have I completed?" | Call `list_tasks` with status "completed" |

## Data Consistency

Across all phases, the Task entity maintains these core attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| id | integer | Unique identifier |
| title | string | Task title (required) |
| description | string | Task description (optional) |
| completed | boolean | Completion status |

---

*This document applies to all phases. Each phase may add additional attributes as specified in their respective constraints.*
