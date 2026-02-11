# Phase 2: Full-Stack Web Application Specification

**Feature Branch**: `phase-2-web-app`
**Created**: 2026-01-09
**Status**: Draft
**Input**: Transform Phase 1 console app to full-stack web app with authentication and persistent storage

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration & Login (Priority: P1)

A user wants to create an account and log in to the todo application. They visit the website, click "Sign Up", provide their email and password, then log in with their credentials.

**Why this priority**: Authentication is the foundation of the multi-user web application. Without it, we cannot isolate user data properly.

**Independent Test**: Navigate to the signup page, register with a new email, verify account creation, then log in with the same credentials.

**Acceptance Scenarios**:

1. **Given** user visits the application, **When** user navigates to signup page and provides valid email and password, **Then** account is created and user is logged in
2. **Given** user has an account, **When** user navigates to login page and provides correct credentials, **Then** user is authenticated and redirected to dashboard
3. **Given** user has an account, **When** user provides incorrect password, **Then** authentication fails with appropriate error message
4. **Given** user has an account, **When** user provides non-existent email, **Then** authentication fails with appropriate error message
5. **Given** user is logged in, **When** user refreshes the page, **Then** user remains authenticated using JWT tokens

---

### User Story 2 - Add Task (Priority: P2)

A user wants to capture a new task they need to complete. They log in to the web application, fill out the task form with a title and optional description, and see the task appear in their list.

**Why this priority**: This is the core functionality carried over from Phase 1 - the fundamental reason users use the app.

**Independent Test**: Log in, add a task with title "Buy groceries" and description "Milk, eggs, bread", verify the task appears in the task list with status "Pending".

**Acceptance Scenarios**:

1. **Given** user is logged in with empty task list, **When** user provides title "Complete project report" and description "Include Q4 metrics", **Then** a new task is created with unique ID, status "Pending", and appears in the task list
2. **Given** user has existing tasks, **When** user adds a new task "Review documentation", **Then** the new task receives a unique ID and appears in the user's task list
3. **Given** the add task form is displayed, **When** user provides title "Quick reminder" with no description, **Then** task is created successfully with empty description field
4. **Given** the add task form is displayed, **When** user attempts to add a task with an empty title, **Then** system displays error "Title cannot be empty" and prevents submission
5. **Given** an existing task titled "Buy groceries", **When** user adds another task also titled "Buy groceries", **Then** both tasks are created with different IDs (duplicate titles are allowed)

---

### User Story 3 - View Tasks (Priority: P3)

A user wants to see all their tasks at a glance to understand what needs to be done. They log in and see a formatted list showing each task's title, description, and status.

**Why this priority**: After adding tasks, users need to view them. This is essential for the application to be useful.

**Independent Test**: Add three tasks (one Pending, one Completed, one with long description), then view all tasks and verify all details are displayed clearly and readably.

**Acceptance Scenarios**:

1. **Given** the user's task list contains 3 tasks with varying titles, descriptions, and statuses, **When** user views the dashboard, **Then** all tasks are displayed showing title, description (or "[No description]" if empty), and status in a readable format
2. **Given** the user's task list is empty, **When** user visits the dashboard, **Then** system displays message "No tasks found. Add your first task to get started!"
3. **Given** a task with a long description, **When** viewing all tasks, **Then** the description is displayed appropriately without breaking the layout
4. **Given** user has many tasks, **When** viewing tasks, **Then** they are displayed with pagination or infinite scroll for performance

---

### User Story 4 - Update Task Details (Priority: P4)

A user realizes they need to change the title or description of an existing task. They log in, find the task in their list, click edit, and provide new details.

**Why this priority**: Users make mistakes or circumstances change. Editing capability improves usability.

**Independent Test**: Add a task "Finsih report" with description "By Friday", then update it to title "Finish report" and description "By Friday EOD", verify changes are reflected in the task list.

**Acceptance Scenarios**:

1. **Given** a task with title "Review code", description "Check for bugs", status "Pending", **When** user updates the task with new title "Review code carefully" and new description "Check for bugs and performance issues", **Then** the task retains its status "Pending", but title and description are updated
2. **Given** a task, **When** user updates only the title to "New Title" and leaves description unchanged, **Then** only the title is updated, description remains the same
3. **Given** a task, **When** user updates only the description and leaves title unchanged, **Then** only the description is updated, title remains the same
4. **Given** user attempts to update a task that doesn't belong to them, **Then** system returns 404 or 403 error and prevents unauthorized access
5. **Given** the update form for title, **When** user provides an empty title, **Then** system displays error "Title cannot be empty" and prevents submission

---

### User Story 5 - Delete Task (Priority: P5)

A user wants to remove a task that is no longer relevant or was added by mistake. They log in, find the task in their list, and click delete to remove it.

**Why this priority**: Cleanup capability keeps the task list manageable.

**Independent Test**: Add three tasks, delete the middle one, verify it no longer appears in the task list and the remaining tasks are still present.

**Acceptance Scenarios**:

1. **Given** user has tasks in their list, **When** user deletes a task, **Then** task is removed from database, no longer appears in task list, and confirmation message is displayed
2. **Given** user attempts to delete a non-existent task, **Then** system displays error "Task not found" 
3. **Given** a user has a single task, **When** user deletes it, **Then** task list becomes empty and appropriate message is displayed
4. **Given** user attempts to delete a task that doesn't belong to them, **Then** system prevents unauthorized deletion

---

### User Story 6 - Mark Task Complete/Incomplete (Priority: P6)

A user finishes a task and wants to mark it as completed, or realizes a completed task needs to be reopened. They log in, find the task in their list, and toggle its completion status.

**Why this priority**: Status tracking provides value for task management.

**Independent Test**: Add a task, mark it as completed and verify status shows "Completed", then mark it incomplete again and verify status returns to "Pending".

**Acceptance Scenarios**:

1. **Given** a task with status "Pending", **When** user marks task as complete, **Then** task's status changes to "Completed" and visual indication updates
2. **Given** a task with status "Completed", **When** user marks task as incomplete, **Then** task's status changes to "Pending" and visual indication updates
3. **Given** user attempts to toggle status of a non-existent task, **Then** system displays error "Task not found"
4. **Given** a task with status "Completed", **When** user marks it complete again, **Then** it remains "Completed" (idempotent operation, no error)
5. **Given** a task with status "Pending", **When** user marks it incomplete again, **Then** it remains "Pending" (idempotent operation, no error)

---

### Edge Cases

- What happens when a user provides a title exceeding 100 characters? System truncates to 100 characters and displays warning "Title truncated to 100 characters"
- What happens when a user provides a description exceeding 500 characters? System truncates to 500 characters and displays warning "Description truncated to 500 characters"
- What happens when a user's JWT token expires? User is redirected to login page
- What happens when user enters invalid input in the UI? Form validation prevents submission and shows appropriate error messages
- What happens with concurrent access? Database transactions prevent race conditions
- What happens when the database is temporarily unavailable? Appropriate error messages are shown to the user

## Requirements *(mandatory)*

### Functional Requirements

**Authentication (FR-001 to FR-005)**:
- **FR-001**: System MUST implement user registration with email and password
- **FR-002**: System MUST implement secure user login with email and password
- **FR-003**: System MUST use JWT tokens for session management
- **FR-004**: System MUST validate JWT tokens on protected API endpoints
- **FR-005**: System MUST associate all tasks with the authenticated user

**Task Creation (FR-006 to FR-010)**:
- **FR-006**: System MUST allow authenticated users to create a new task by providing a title (required) and description (optional)
- **FR-007**: System MUST assign a unique, auto-incrementing integer ID to each new task
- **FR-008**: System MUST validate that task title is not empty (after trimming whitespace) before creating the task
- **FR-009**: System MUST set the default status of newly created tasks to "Pending"
- **FR-010**: System MUST allow duplicate task titles (multiple tasks can have the same title)

**Task Viewing (FR-011 to FR-013)**:
- **FR-011**: System MUST display only tasks belonging to the authenticated user
- **FR-012**: System MUST display all tasks showing title, description, and status in a readable format
- **FR-013**: System MUST display tasks sorted by creation date (most recent first) by default

**Task Updating (FR-014 to FR-016)**:
- **FR-014**: System MUST allow users to update the title and/or description of their existing tasks
- **FR-015**: System MUST preserve the task's ID and ownership when updating title or description
- **FR-016**: System MUST validate that the new title (if being updated) is not empty

**Task Deletion (FR-017 to FR-018)**:
- **FR-017**: System MUST allow users to delete their own tasks
- **FR-018**: System MUST remove the task completely from database when deleted

**Task Status Management (FR-019 to FR-020)**:
- **FR-019**: System MUST allow users to toggle a task's status between "Pending" and "Completed"
- **FR-020**: System MUST change status from "Pending" to "Completed" when user marks a task complete

**Data Constraints (FR-021 to FR-022)**:
- **FR-021**: System MUST limit task title to a maximum of 100 characters, truncating with a warning if exceeded
- **FR-022**: System MUST limit task description to a maximum of 500 characters, truncating with a warning if exceeded

**User Interface (FR-023 to FR-025)**:
- **FR-023**: System MUST provide a responsive web interface compatible with desktop and mobile devices
- **FR-024**: System MUST display clear error messages in user-friendly language
- **FR-025**: System MUST provide visual feedback during API requests (loading states)

### Technical Requirements

**Frontend (TR-001 to TR-005)**:
- **TR-001**: Frontend MUST be built with Next.js 16+ using App Router
- **TR-002**: Frontend MUST use TypeScript for type safety
- **TR-003**: Frontend MUST use Tailwind CSS for styling
- **TR-004**: Frontend MUST implement Better Auth for authentication
- **TR-005**: Frontend MUST make API calls to the backend using fetch or axios

**Backend (TR-006 to TR-010)**:
- **TR-006**: Backend MUST be built with Python FastAPI
- **TR-007**: Backend MUST use SQLModel as the ORM
- **TR-008**: Backend MUST connect to Neon Serverless PostgreSQL database
- **TR-009**: Backend MUST implement JWT token validation middleware
- **TR-010**: Backend MUST implement RESTful API endpoints following standard conventions

**Database (TR-011 to TR-013)**:
- **TR-011**: Database MUST store user accounts with encrypted passwords
- **TR-012**: Database MUST store tasks with foreign key relationship to users
- **TR-013**: Database MUST include indexes for efficient querying of user-specific tasks

**Security (TR-014 to TR-016)**:
- **TR-014**: System MUST validate JWT tokens on all protected endpoints
- **TR-015**: System MUST enforce user data isolation (users can only access their own tasks)
- **TR-016**: System MUST implement proper input validation and sanitization

### Key Entities

- **User**: Represents an authenticated user with the following attributes:
  - **id** (string): Unique identifier from Better Auth
  - **email** (string): User's email address (unique)
  - **name** (string): User's name (optional)
  - **created_at** (datetime): Account creation timestamp

- **Task**: Represents a single todo item with the following attributes:
  - **id** (integer): Unique identifier, auto-generated sequentially, immutable after creation
  - **user_id** (string): Foreign key linking to the user who owns the task
  - **title** (string): Required, 1-100 characters, describes the task
  - **description** (string): Optional, 0-500 characters, provides additional task details
  - **completed** (boolean): Task completion status, default is false
  - **created_at** (datetime): Task creation timestamp
  - **updated_at** (datetime): Last update timestamp

### Assumptions

- Users interact with the application through a modern web browser
- The application uses a client-server architecture with API communication
- Better Auth manages user sessions and JWT token issuance
- Neon PostgreSQL database is properly configured and accessible
- Network connectivity exists between frontend and backend
- JWT tokens have a reasonable expiration time (e.g., 7 days)
- The application follows RESTful API design principles

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can register and log in within 60 seconds
- **SC-002**: Users can add a new task in under 30 seconds from the dashboard
- **SC-003**: Users can view all their tasks in under 5 seconds from navigating to the dashboard
- **SC-004**: Task list displays correctly with up to 100 tasks without performance degradation
- **SC-005**: 100% of valid task operations (add, view, update, delete, mark status) complete successfully without crashes
- **SC-006**: Invalid operations (empty title, unauthorized access) display clear error messages within 2 seconds
- **SC-007**: Users can complete a full task workflow (register → login → add → view → update → mark complete → delete) in under 5 minutes
- **SC-008**: Application handles edge cases (empty list, expired tokens) gracefully without crashes
- **SC-009**: New users can understand how to perform all operations within 5 minutes of first use
- **SC-010**: API endpoints return appropriate HTTP status codes (200, 400, 401, 403, 404, 500)
- **SC-011**: Frontend displays appropriate loading states during API requests
- **SC-012**: Mobile responsiveness works on screens down to 320px width