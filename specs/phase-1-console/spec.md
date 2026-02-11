# Feature Specification: Core Todo Operations

**Feature Branch**: `001-core-features`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "All core features: Add, View, Update, Delete, and Mark Complete/Incomplete tasks"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

A user wants to capture a new task they need to complete. They launch the application, select the option to add a task, provide a title and optional description, and see confirmation that the task was created.

**Why this priority**: This is the foundational capability - without the ability to add tasks, the application has no purpose. This is the minimum viable product (MVP).

**Independent Test**: Launch the app, add a task with title "Buy groceries" and description "Milk, eggs, bread", verify the task appears in the task list with a unique ID and status "Pending".

**Acceptance Scenarios**:

1. **Given** the application is running with an empty task list, **When** user provides title "Complete project report" and description "Include Q4 metrics", **Then** a new task is created with unique ID 1, status "Pending", and appears in the task list
2. **Given** existing tasks with IDs 1-3, **When** user adds a new task "Review documentation", **Then** the new task receives ID 4 (sequential after highest existing ID)
3. **Given** the application prompts for task details, **When** user provides title "Quick reminder" with no description (empty/blank), **Then** task is created successfully with empty description field
4. **Given** the add task prompt is displayed, **When** user attempts to add a task with an empty title (blank or only whitespace), **Then** system displays error "Title cannot be empty" and prompts again
5. **Given** an existing task titled "Buy groceries", **When** user adds another task also titled "Buy groceries", **Then** both tasks are created with different IDs (duplicate titles are allowed)

---

### User Story 2 - View All Tasks (Priority: P2)

A user wants to see all their tasks at a glance to understand what needs to be done. They select the view option and see a formatted list showing each task's ID, title, description, and status.

**Why this priority**: After adding tasks, users need to view them. This is essential for the application to be useful, making it the second priority.

**Independent Test**: Add three tasks (one Pending, one Completed, one with long description), then view all tasks and verify all details (ID, title, description, status) are displayed clearly and readably.

**Acceptance Scenarios**:

1. **Given** the task list contains 3 tasks with varying titles, descriptions, and statuses, **When** user selects "View Tasks", **Then** all tasks are displayed showing ID, title, description (or "[No description]" if empty), and status in a readable format
2. **Given** the task list is empty, **When** user selects "View Tasks", **Then** system displays message "No tasks found. Add your first task to get started!"
3. **Given** a task with a 300-character description, **When** viewing all tasks, **Then** the full description is displayed without truncation
4. **Given** tasks with IDs 1, 3, 5 (non-sequential due to deletions), **When** viewing tasks, **Then** all tasks are displayed sorted by ID in ascending order

---

### User Story 3 - Update Task Details (Priority: P3)

A user realizes they need to change the title or description of an existing task. They select the update option, specify which task by ID, and provide new details.

**Why this priority**: Users make mistakes or circumstances change. Editing capability improves usability but is not critical for basic functionality.

**Independent Test**: Add a task "Finsih report" with description "By Friday", then update it to title "Finish report" and description "By Friday EOD", verify changes are reflected in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 2, title "Review code", description "Check for bugs", status "Pending", **When** user updates the task with new title "Review code carefully" and new description "Check for bugs and performance issues", **Then** the task retains ID 2 and status "Pending", but title and description are updated
2. **Given** a task with ID 5, **When** user updates only the title to "New Title" and leaves description unchanged, **Then** only the title is updated, description remains the same
3. **Given** a task with ID 3, **When** user updates only the description and leaves title unchanged, **Then** only the description is updated, title remains the same
4. **Given** the update prompt, **When** user enters a non-existent task ID (e.g., 99), **Then** system displays error "Task ID 99 not found" and returns to main menu
5. **Given** the update prompt for title, **When** user provides an empty title (blank or whitespace only), **Then** system displays error "Title cannot be empty" and prompts again without updating the task

---

### User Story 4 - Delete Task (Priority: P4)

A user wants to remove a task that is no longer relevant or was added by mistake. They select the delete option, specify the task ID, and receive confirmation that the task was removed.

**Why this priority**: Cleanup capability keeps the task list manageable but is less critical than creating, viewing, and editing tasks.

**Independent Test**: Add three tasks, delete the middle one (ID 2), verify it no longer appears in the task list and the remaining tasks (IDs 1 and 3) are still present.

**Acceptance Scenarios**:

1. **Given** tasks with IDs 1, 2, 3, **When** user deletes task ID 2, **Then** task 2 is removed from memory, view shows only tasks 1 and 3, and confirmation message "Task ID 2 deleted successfully" is displayed
2. **Given** the delete prompt, **When** user enters a non-existent task ID (e.g., 99), **Then** system displays error "Task ID 99 not found" and returns to main menu without deleting anything
3. **Given** a single task with ID 1, **When** user deletes it, **Then** task list becomes empty and viewing tasks shows "No tasks found" message
4. **Given** tasks 1, 3, 5 exist, **When** user adds a new task after deletion, **Then** the new task receives the next sequential ID (6), not filling gaps

---

### User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

A user finishes a task and wants to mark it as completed, or realizes a completed task needs to be reopened. They select the mark complete/incomplete option, specify the task ID, and see the status toggle.

**Why this priority**: Status tracking provides value but is not essential for basic task management. Users can still use the app effectively by deleting completed tasks instead.

**Independent Test**: Add a task, mark it as completed and verify status shows "Completed", then mark it incomplete again and verify status returns to "Pending".

**Acceptance Scenarios**:

1. **Given** a task with ID 2 and status "Pending", **When** user marks task 2 as complete, **Then** task 2's status changes to "Completed" and confirmation message "Task ID 2 marked as Completed" is displayed
2. **Given** a task with ID 4 and status "Completed", **When** user marks task 4 as incomplete, **Then** task 4's status changes to "Pending" and confirmation message "Task ID 4 marked as Pending" is displayed
3. **Given** the mark status prompt, **When** user enters a non-existent task ID (e.g., 99), **Then** system displays error "Task ID 99 not found" and returns to main menu without changing any status
4. **Given** a task with status "Completed", **When** user marks it complete again, **Then** it remains "Completed" (idempotent operation, no error)
5. **Given** a task with status "Pending", **When** user marks it incomplete again, **Then** it remains "Pending" (idempotent operation, no error)

---

### Edge Cases

- What happens when a user provides a title exceeding 100 characters? System truncates to 100 characters and displays warning "Title truncated to 100 characters"
- What happens when a user provides a description exceeding 500 characters? System truncates to 500 characters and displays warning "Description truncated to 500 characters"
- What happens when the application restarts? All tasks are lost (in-memory storage), user sees empty task list with message "No tasks found"
- What happens when user enters invalid input at the main menu (e.g., letter instead of number)? System displays "Invalid choice. Please try again." and re-displays menu
- What happens with very large task IDs (e.g., after 10,000 tasks added and deleted)? System continues incrementing ID without issues (Python integers have arbitrary precision)
- What happens if user tries to enter multi-line input where single-line is expected? Behavior depends on input method - default Python input() takes first line only

## Requirements *(mandatory)*

### Functional Requirements

**Task Creation (FR-001 to FR-005)**:
- **FR-001**: System MUST allow users to create a new task by providing a title (required) and description (optional)
- **FR-002**: System MUST assign a unique, auto-incrementing integer ID to each new task, starting from 1
- **FR-003**: System MUST validate that task title is not empty (after trimming whitespace) before creating the task
- **FR-004**: System MUST set the default status of newly created tasks to "Pending"
- **FR-005**: System MUST allow duplicate task titles (multiple tasks can have the same title)

**Task Viewing (FR-006 to FR-008)**:
- **FR-006**: System MUST display all tasks showing ID, title, description, and status in a readable format
- **FR-007**: System MUST display tasks sorted by ID in ascending order
- **FR-008**: System MUST show a friendly message "No tasks found. Add your first task to get started!" when the task list is empty

**Task Updating (FR-009 to FR-012)**:
- **FR-009**: System MUST allow users to update the title and/or description of an existing task by specifying its ID
- **FR-010**: System MUST preserve the task's ID and status when updating title or description
- **FR-011**: System MUST validate that the new title (if being updated) is not empty
- **FR-012**: System MUST display error message "Task ID {id} not found" when user attempts to update a non-existent task

**Task Deletion (FR-013 to FR-015)**:
- **FR-013**: System MUST allow users to delete a task by specifying its ID
- **FR-014**: System MUST remove the task completely from memory when deleted
- **FR-015**: System MUST display error message "Task ID {id} not found" when user attempts to delete a non-existent task

**Task Status Management (FR-016 to FR-018)**:
- **FR-016**: System MUST allow users to toggle a task's status between "Pending" and "Completed" by specifying its ID
- **FR-017**: System MUST change status from "Pending" to "Completed" when user marks a task complete
- **FR-018**: System MUST change status from "Completed" to "Pending" when user marks a task incomplete

**Data Constraints (FR-019 to FR-021)**:
- **FR-019**: System MUST limit task title to a maximum of 100 characters, truncating with a warning if exceeded
- **FR-020**: System MUST limit task description to a maximum of 500 characters, truncating with a warning if exceeded
- **FR-021**: System MUST use only in-memory storage (Python data structures like lists or dictionaries), with all data lost when the application terminates

**User Interface (FR-022 to FR-025)**:
- **FR-022**: System MUST provide a console-based menu interface for users to select operations
- **FR-023**: System MUST display clear prompts for all user inputs (task details, IDs, menu choices)
- **FR-024**: System MUST display error messages in user-friendly language without technical stack traces
- **FR-025**: System MUST return to the main menu after completing each operation or encountering an error

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - **ID** (integer): Unique identifier, auto-generated sequentially starting from 1, immutable after creation
  - **Title** (string): Required, 1-100 characters, describes the task
  - **Description** (string): Optional, 0-500 characters, provides additional task details
  - **Status** (string): Either "Pending" or "Completed" (case-sensitive), default is "Pending"

### Assumptions

- Users interact with the application through a standard terminal/console that supports text input and output
- The application runs as a single-user, single-session program (no concurrent users)
- Task IDs never reset during a session, even after deletions (always increment)
- When a task is deleted, its ID is not reused for new tasks
- Input validation happens immediately when user provides input, not deferred
- Status values are exactly "Pending" and "Completed" with that exact capitalization
- Empty descriptions are stored as empty strings (not null or placeholder text)
- Application does not persist state between runs (fresh start each time)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task (title and description) in under 30 seconds from launching the application
- **SC-002**: Users can view all tasks in under 5 seconds from selecting the view option
- **SC-003**: Task list displays correctly with up to 100 tasks without performance degradation or formatting issues
- **SC-004**: 100% of valid task operations (add, view, update, delete, mark status) complete successfully without crashes
- **SC-005**: Invalid operations (wrong ID, empty title) display clear error messages within 2 seconds and allow user to retry
- **SC-006**: Users can complete a full task workflow (add → view → update → mark complete → delete) in under 2 minutes
- **SC-007**: Application handles edge cases (empty list, non-existent IDs, duplicate titles) gracefully without crashes
- **SC-008**: New users can understand how to perform all five core operations within 5 minutes of first use (based on menu clarity)
