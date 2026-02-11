# Quickstart Guide: Core Todo Operations

**Feature**: Core Todo Operations
**Created**: 2026-01-01
**Purpose**: Manual testing scenarios for validating all core functionality

## Prerequisites

- Python 3.8 or higher installed
- No external dependencies required
- Source file: `src/todo_app.py`

## Running the Application

```bash
# From repository root
python src/todo_app.py
```

Expected output: Main menu with 6 options displayed.

## Test Scenarios

### Scenario 1: Add Task - Happy Path (US1)

**Objective**: Verify task creation with valid inputs

**Steps**:
1. Launch application: `python src/todo_app.py`
2. Select option `1` (Add Task)
3. Enter title: `Buy groceries`
4. Enter description: `Milk, eggs, bread`
5. Select option `2` (View Tasks) to verify

**Expected Results**:
- Task created with ID `1`
- Title: "Buy groceries"
- Description: "Milk, eggs, bread"
- Status: "Pending"
- Task appears in view list

**Pass/Fail**: _______

---

### Scenario 2: Add Task - Empty Description (US1)

**Objective**: Verify task creation with no description

**Steps**:
1. Select option `1` (Add Task)
2. Enter title: `Quick reminder`
3. Press Enter without typing description (leave empty)
4. Select option `2` (View Tasks)

**Expected Results**:
- Task created successfully with next available ID
- Title: "Quick reminder"
- Description displayed as "[No description]" or empty
- Status: "Pending"

**Pass/Fail**: _______

---

### Scenario 3: Add Task - Empty Title (US1 - Error Case)

**Objective**: Verify empty title validation

**Steps**:
1. Select option `1` (Add Task)
2. Press Enter without typing title (or enter only spaces)
3. Observe error message

**Expected Results**:
- Error message: "Title cannot be empty"
- Application re-prompts for title (does not create task)
- No task added to list

**Pass/Fail**: _______

---

### Scenario 4: Add Task - Duplicate Titles (US1)

**Objective**: Verify duplicate titles are allowed

**Steps**:
1. Select option `1` and add task "Buy groceries" (if not already exists)
2. Select option `1` again and add another task "Buy groceries"
3. Select option `2` (View Tasks)

**Expected Results**:
- Two separate tasks both titled "Buy groceries"
- Different task IDs (e.g., 1 and 2)
- Both tasks visible in list

**Pass/Fail**: _______

---

### Scenario 5: Add Task - Title Truncation (Edge Case)

**Objective**: Verify title truncation at 100 characters

**Steps**:
1. Select option `1` (Add Task)
2. Enter a title longer than 100 characters (e.g., paste 150 characters)
3. Observe warning message

**Expected Results**:
- Warning: "Title truncated to 100 characters"
- Task created with title exactly 100 characters long
- Description prompt appears normally

**Pass/Fail**: _______

---

### Scenario 6: View Tasks - Multiple Tasks (US2)

**Objective**: Verify viewing multiple tasks with different statuses

**Setup**: Add 3 tasks (if not already present):
- Task 1: "Buy groceries", "Milk, eggs", Pending
- Task 2: "Finish report", "", Completed (mark complete manually)
- Task 3: "Call dentist", "Schedule checkup", Pending

**Steps**:
1. Select option `2` (View Tasks)

**Expected Results**:
- All 3 tasks displayed
- Sorted by ID (ascending: 1, 2, 3)
- Each shows: ID, Title, Description (or "[No description]"), Status
- Readable format (clear separation between tasks)

**Pass/Fail**: _______

---

### Scenario 7: View Tasks - Empty List (US2)

**Objective**: Verify viewing when no tasks exist

**Setup**: Start fresh application (no tasks added yet)

**Steps**:
1. Select option `2` (View Tasks) immediately after launch

**Expected Results**:
- Message: "No tasks found. Add your first task to get started!"
- No error or crash
- Returns to main menu

**Pass/Fail**: _______

---

### Scenario 8: Update Task - Change Title and Description (US3)

**Objective**: Verify updating both fields

**Setup**: Add task with ID 1: "Finsih report", "By Friday", Pending

**Steps**:
1. Select option `3` (Update Task)
2. Enter task ID: `1`
3. Enter new title: `Finish report` (corrected spelling)
4. Enter new description: `By Friday EOD`
5. Select option `2` (View Tasks) to verify

**Expected Results**:
- Task ID 1 still exists
- Title updated to: "Finish report"
- Description updated to: "By Friday EOD"
- Status unchanged: "Pending"

**Pass/Fail**: _______

---

### Scenario 9: Update Task - Invalid ID (US3 - Error Case)

**Objective**: Verify error handling for non-existent task

**Steps**:
1. Select option `3` (Update Task)
2. Enter task ID: `99` (assuming this ID doesn't exist)

**Expected Results**:
- Error message: "Task ID 99 not found"
- No crash or exception
- Returns to main menu

**Pass/Fail**: _______

---

### Scenario 10: Update Task - Empty Title (US3 - Error Case)

**Objective**: Verify title validation during update

**Setup**: Task ID 1 exists

**Steps**:
1. Select option `3` (Update Task)
2. Enter task ID: `1`
3. Press Enter for title without typing (leave empty)

**Expected Results**:
- Error message: "Title cannot be empty"
- Application re-prompts for title
- Task not updated

**Pass/Fail**: _______

---

### Scenario 11: Delete Task - Middle Task (US4)

**Objective**: Verify deletion and ID gap handling

**Setup**: Tasks with IDs 1, 2, 3 exist

**Steps**:
1. Select option `4` (Delete Task)
2. Enter task ID: `2`
3. Observe confirmation message
4. Select option `2` (View Tasks)

**Expected Results**:
- Confirmation: "Task ID 2 deleted successfully"
- Task 2 no longer appears in list
- Tasks 1 and 3 still present
- IDs remain 1 and 3 (gap at 2)

**Pass/Fail**: _______

---

### Scenario 12: Delete Task - Invalid ID (US4 - Error Case)

**Objective**: Verify error handling for non-existent task

**Steps**:
1. Select option `4` (Delete Task)
2. Enter task ID: `99`

**Expected Results**:
- Error message: "Task ID 99 not found"
- No crash
- Returns to main menu
- No tasks deleted

**Pass/Fail**: _______

---

### Scenario 13: Delete Task - ID Not Reused (US4)

**Objective**: Verify deleted IDs are not reused

**Setup**: Tasks 1, 2, 3 exist. Delete task 2.

**Steps**:
1. After deleting task 2, select option `1` (Add Task)
2. Add new task: "New task"
3. Select option `2` (View Tasks)

**Expected Results**:
- New task receives ID `4` (not ID 2)
- Task list shows IDs: 1, 3, 4 (gap at 2 remains)

**Pass/Fail**: _______

---

### Scenario 14: Mark Complete (US5)

**Objective**: Verify marking task as completed

**Setup**: Task ID 1 exists with status "Pending"

**Steps**:
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `1`
3. Choose to mark as complete
4. Select option `2` (View Tasks)

**Expected Results**:
- Confirmation: "Task ID 1 marked as Completed"
- Task 1 status changed to "Completed"
- Title and description unchanged

**Pass/Fail**: _______

---

### Scenario 15: Mark Incomplete (US5)

**Objective**: Verify marking task as pending

**Setup**: Task ID 1 exists with status "Completed"

**Steps**:
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `1`
3. Choose to mark as incomplete
4. Select option `2` (View Tasks)

**Expected Results**:
- Confirmation: "Task ID 1 marked as Pending"
- Task 1 status changed to "Pending"
- Title and description unchanged

**Pass/Fail**: _______

---

### Scenario 16: Mark Status - Invalid ID (US5 - Error Case)

**Objective**: Verify error handling for non-existent task

**Steps**:
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `99`

**Expected Results**:
- Error message: "Task ID 99 not found"
- No crash
- Returns to main menu
- No status changes

**Pass/Fail**: _______

---

### Scenario 17: Mark Status - Idempotent (US5)

**Objective**: Verify marking completed task as completed (no error)

**Setup**: Task ID 1 exists with status "Completed"

**Steps**:
1. Select option `5` (Mark Complete/Incomplete)
2. Enter task ID: `1`
3. Choose to mark as complete (already completed)

**Expected Results**:
- Task remains "Completed" (no error message)
- Confirmation message displayed normally
- Operation succeeds without warnings

**Pass/Fail**: _______

---

### Scenario 18: Invalid Menu Choice (Edge Case)

**Objective**: Verify menu input validation

**Steps**:
1. At main menu, enter `abc` (letters instead of number)
2. Observe error message

**Expected Results**:
- Error message: "Invalid choice. Please try again."
- Main menu re-displayed
- Application continues running (no crash)

**Pass/Fail**: _______

---

### Scenario 19: Data Persistence - Restart (Edge Case)

**Objective**: Verify in-memory storage (data loss on exit)

**Setup**: Add 2-3 tasks

**Steps**:
1. Exit application (option `6`)
2. Restart application: `python src/todo_app.py`
3. Select option `2` (View Tasks)

**Expected Results**:
- Message: "No tasks found. Add your first task to get started!"
- All previous tasks lost
- Next task ID starts at `1` again

**Pass/Fail**: _______

---

### Scenario 20: Full Workflow (Integration Test)

**Objective**: Verify complete add → view → update → complete → delete workflow

**Steps**:
1. Add task: "Complete project", "Due next week", Pending
2. View tasks (verify task exists with ID 1)
3. Update task 1: "Complete project report", "Due next Friday"
4. View tasks (verify update)
5. Mark task 1 complete
6. View tasks (verify status "Completed")
7. Delete task 1
8. View tasks (verify empty list)

**Expected Results**:
- All operations complete successfully
- Each step reflects correct state
- No errors or crashes throughout workflow
- Returns to menu after each operation

**Pass/Fail**: _______

---

## Summary Report

**Total Scenarios**: 20
**Passed**: _______
**Failed**: _______
**Blocked**: _______

**Notes/Issues**:

---

**Tester**: _____________
**Date**: _____________
**Application Version**: _____________
