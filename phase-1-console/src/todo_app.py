"""
In-Memory Todo Console Application

A beginner-friendly task management application that demonstrates Python fundamentals
through practical implementation. Features include adding, viewing, updating, deleting,
and marking tasks as complete/incomplete.

All data is stored in-memory and lost when the application terminates.
No external dependencies required - uses Python standard library only.

Usage:
    python src/todo_app.py

Features:
    1. Add Task - Create new tasks with title and optional description
    2. View Tasks - Display all tasks sorted by ID
    3. Update Task - Modify title and/or description of existing tasks
    4. Delete Task - Remove tasks by ID
    5. Mark Complete/Incomplete - Toggle task status
    6. Exit - Terminate the application

Author: Generated with Claude Code
Version: 1.1.0 (Visual Enhancement)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL STYLING - ANSI Color Codes (Windows CMD/PowerShell Compatible)
# ═══════════════════════════════════════════════════════════════════════════════

# Colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Foreground Colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright Foreground Colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background Colors
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"

# ═══════════════════════════════════════════════════════════════════════════════
# ICONS AND SYMBOLS
# ═══════════════════════════════════════════════════════════════════════════════

# Status Icons
ICON_COMPLETED = "✅"
ICON_PENDING = "🔹"
ICON_TODO = "📋"
ICON_ADD = "➕"
ICON_VIEW = "🔍"
ICON_EDIT = "✏️"
ICON_DELETE = "🗑️"
ICON_TOGGLE = "🔄"
ICON_EXIT = "🚪"
ICON_HOME = "🏠"
ICON_WARN = "⚠️"
ICON_ERROR = "❌"
ICON_SUCCESS = "✓"
ICON_INFO = "ℹ️"
ICON_SEARCH = "🔎"
ICON_CALENDAR = "📅"
ICON_CLOCK = "⏰"
ICON_BULLET = "•"
ICON_ARROW_RIGHT = "→"
ICON_CHECKBOX_EMPTY = "☐"
ICON_CHECKBOX_CHECKED = "☑"

# Box Drawing Characters
BOX_HORIZONTAL = "─"
BOX_VERTICAL = "│"
BOX_CORNER_TOP_LEFT = "┌"
BOX_CORNER_TOP_RIGHT = "┐"
BOX_CORNER_BOTTOM_LEFT = "└"
BOX_CORNER_BOTTOM_RIGHT = "┘"
BOX_T_DOWN = "┬"
BOX_T_UP = "┴"
BOX_T_RIGHT = "├"
BOX_T_LEFT = "┤"
BOX_CROSS = "┼"

# Decorative Lines
LINE_THICK = "═" * 60
LINE_MEDIUM = "─" * 50
LINE_THIN = "·" * 40

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATTING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════


def color(text, color_code):
    """Apply color to text."""
    return f"{color_code}{text}{RESET}"


def bold(text):
    """Apply bold styling."""
    return f"{BOLD}{text}{RESET}"


def section_header(title, icon=""):
    """Create a styled section header."""
    if icon:
        return f"\n{color(icon, CYAN)} {bold(color(title, BRIGHT_CYAN))}"
    return f"\n{bold(color(title, BRIGHT_CYAN))}"


def success_msg(msg):
    """Display a success message."""
    return f"  {color(ICON_SUCCESS, GREEN)} {color(msg, GREEN)}"


def error_msg(msg):
    """Display an error message."""
    return f"  {color(ICON_ERROR, RED)} {color(msg, RED)}"


def warn_msg(msg):
    """Display a warning message."""
    return f"  {color(ICON_WARN, YELLOW)} {color(msg, YELLOW)}"


def info_msg(msg):
    """Display an info message."""
    return f"  {color(ICON_INFO, BLUE)} {color(msg, BLUE)}"


def status_badge(status):
    """Create a colored status badge."""
    if status == "Completed":
        return f"{ICON_COMPLETED} {color('Completed', GREEN)}"
    else:
        return f"{ICON_PENDING} {color('Pending', BRIGHT_BLUE)}"


def draw_box(content, width=50):
    """Draw a box around content."""
    lines = content.split('\n')
    box = []
    box.append(f"{color(BOX_CORNER_TOP_LEFT, CYAN)}{BOX_HORIZONTAL * (width - 2)}{color(BOX_CORNER_TOP_RIGHT, CYAN)}")
    for line in lines:
        box.append(f"{color(BOX_VERTICAL, CYAN)} {line:<{width - 4}} {color(BOX_VERTICAL, CYAN)}")
    box.append(f"{color(BOX_CORNER_BOTTOM_LEFT, CYAN)}{BOX_HORIZONTAL * (width - 2)}{color(BOX_CORNER_BOTTOM_RIGHT, CYAN)}")
    return '\n'.join(box)


def draw_menu_item(number, icon, label, description=""):
    """Draw a styled menu item."""
    if description:
        return f"  {color(number, BRIGHT_YELLOW)}. {icon} {color(label, WHITE)}  {color(DIM + description + RESET, DIM)}"
    return f"  {color(number, BRIGHT_YELLOW)}. {icon} {color(label, WHITE)}"


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL DATA STORAGE
# ═══════════════════════════════════════════════════════════════════════════════

# Global data storage (in-memory only)
task_store = {}  # Dictionary: {task_id: {"id": int, "title": str, "description": str, "status": str}}
next_task_id = 1  # Counter for generating unique task IDs


def get_user_input(prompt, allow_empty=False):
    """
    Get user input with optional empty validation.

    Args:
        prompt (str): The prompt message to display to the user
        allow_empty (bool): Whether to allow empty input (default: False)

    Returns:
        str: The user's input (stripped of leading/trailing whitespace)

    Note:
        If allow_empty is False and user provides empty input, will re-prompt.
    """
    while True:
        user_input = input(prompt).strip()
        if not allow_empty and not user_input:
            continue
        return user_input


def validate_title(title):
    """
    Validate and normalize task title.

    Args:
        title (str): The title to validate

    Returns:
        tuple: (validated_title, warning_message or None)

    Rules:
        - Must not be empty after stripping whitespace
        - Maximum 100 characters (truncates with warning if exceeded)
    """
    title = title.strip()

    if not title:
        return None, "Title cannot be empty"

    if len(title) > 100:
        title = title[:100]
        return title, "Title truncated to 100 characters"

    return title, None


def validate_description(description):
    """
    Validate and normalize task description.

    Args:
        description (str): The description to validate

    Returns:
        tuple: (validated_description, warning_message or None)

    Rules:
        - Can be empty (optional field)
        - Maximum 500 characters (truncates with warning if exceeded)
    """
    if len(description) > 500:
        description = description[:500]
        return description, "Description truncated to 500 characters"

    return description, None


def find_task(task_id):
    """
    Look up a task by ID with error handling.

    Args:
        task_id (int): The ID of the task to find

    Returns:
        dict or None: The task dictionary if found, None otherwise

    Note:
        Displays error message if task not found.
    """
    if task_id in task_store:
        return task_store[task_id]
    else:
        print(f"Task ID {task_id} not found")
        return None


def display_menu():
    """
    Display the main menu options with styled formatting.

    Shows all 6 available operations for the user to choose from.
    """
    print(f"\n{color(BOX_CORNER_TOP_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {bold(color('📋 TODO CONSOLE APPLICATION', BRIGHT_CYAN)):<52} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_T_RIGHT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_T_LEFT, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('1', ICON_ADD, 'Add Task', 'Create a new task')}{' ' * 32} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('2', ICON_VIEW, 'View Tasks', 'See all your tasks')}{' ' * 30} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('3', ICON_EDIT, 'Update Task', 'Modify task details')}{' ' * 29} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('4', ICON_DELETE, 'Delete Task', 'Remove a task')}{' ' * 32} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('5', ICON_TOGGLE, 'Mark Complete/Incomplete', 'Toggle status')}{' ' * 18} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {draw_menu_item('6', ICON_EXIT, 'Exit', 'Close the application')}{' ' * 30} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, CYAN)}")


def add_task():
    """
    Add a new task with title and optional description.

    Prompts user for task details, validates input, generates unique ID,
    and stores the task with default status "Pending".

    User Story: US1 (Priority P1) - Add New Task
    """
    global next_task_id

    print(f"\n{color(BOX_CORNER_TOP_LEFT, GREEN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, GREEN)}")
    print(f"{color(BOX_VERTICAL, GREEN)}  {ICON_ADD} {bold(color('ADD NEW TASK', BRIGHT_GREEN)):<50} {color(BOX_VERTICAL, GREEN)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, GREEN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, GREEN)}")

    # Get and validate title
    while True:
        title_input = input(f"\n  {color(ICON_BULLET, YELLOW)} {color('Enter task title:', WHITE)} ").strip()
        validated_title, warning = validate_title(title_input)

        if validated_title is None:
            print(error_msg(warning))
            continue

        if warning:
            print(warn_msg(warning))

        break

    # Get and validate description
    description_input = input(f"  {color(ICON_BULLET, YELLOW)} {color('Enter task description (optional, press Enter to skip):', WHITE)} ")
    validated_description, warning = validate_description(description_input)

    if warning:
        print(warn_msg(warning))

    # Create task
    task = {
        "id": next_task_id,
        "title": validated_title,
        "description": validated_description,
        "status": "Pending"
    }

    # Store task
    task_store[next_task_id] = task
    next_task_id += 1

    # Confirmation
    print(f"\n  {color(ICON_SUCCESS, GREEN)} {color('Task created successfully!', BRIGHT_GREEN)}")
    print(f"  {color(ICON_TODO, CYAN)} {color('ID:', BRIGHT_CYAN)} {color(str(task['id']), BRIGHT_YELLOW)}")
    print(f"  {color(ICON_EDIT, CYAN)} {color('Title:', BRIGHT_CYAN)} {task['title']}")
    print(f"  {status_badge(task['status'])}")


def view_tasks():
    """
    Display all tasks sorted by ID.

    Shows ID, title, description (or "[No description]"), and status
    for each task in a readable format.

    User Story: US2 (Priority P2) - View All Tasks
    """
    print(f"\n{color(BOX_CORNER_TOP_LEFT, BLUE)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, BLUE)}")
    print(f"{color(BOX_VERTICAL, BLUE)}  {ICON_VIEW} {bold(color('ALL TASKS', BRIGHT_BLUE)):<51} {color(BOX_VERTICAL, BLUE)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, BLUE)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, BLUE)}")

    # Check if task store is empty
    if not task_store:
        print(f"\n  {color(ICON_INFO, BRIGHT_BLUE)} {color('No tasks found.', BRIGHT_WHITE)}")
        print(f"  {color(ICON_ADD, CYAN)} {color('Add your first task to get started!', DIM)}")
        return

    # Get sorted task IDs
    sorted_ids = sorted(task_store.keys())

    # Display each task
    for task_id in sorted_ids:
        task = task_store[task_id]
        description = task["description"] if task["description"] else color("[No description]", DIM)

        # Status indicator with checkbox
        checkbox = ICON_CHECKBOX_CHECKED if task["status"] == "Completed" else ICON_CHECKBOX_EMPTY
        status_color = GREEN if task["status"] == "Completed" else BRIGHT_BLUE

        print(f"\n  {color(checkbox, status_color)} {color(f'Task #{task["id"]}', BRIGHT_YELLOW)} {status_badge(task['status'])}")
        print(f"  {color(BOX_VERTICAL, CYAN)} {color('Title:', BRIGHT_CYAN)} {task['title']}")
        print(f"  {color(BOX_VERTICAL, CYAN)} {color('Description:', BRIGHT_CYAN)} {description}")

    # Summary footer
    print(f"\n{color(BOX_T_RIGHT, BLUE)}{BOX_HORIZONTAL * 56}{color(BOX_T_LEFT, BLUE)}")
    pending_count = sum(1 for t in task_store.values() if t["status"] == "Pending")
    completed_count = sum(1 for t in task_store.values() if t["status"] == "Completed")
    print(f"{color(BOX_VERTICAL, BLUE)}  {ICON_TODO} {color('Total Tasks:', BRIGHT_CYAN)} {color(str(len(task_store)), BRIGHT_YELLOW)}")
    print(f"{color(BOX_VERTICAL, BLUE)}    {color(ICON_PENDING, BRIGHT_BLUE)} {color('Pending:', BRIGHT_BLUE)} {color(str(pending_count), BRIGHT_YELLOW)}")
    print(f"{color(BOX_VERTICAL, BLUE)}    {color(ICON_COMPLETED, GREEN)} {color('Completed:', GREEN)} {color(str(completed_count), BRIGHT_YELLOW)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, BLUE)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, BLUE)}")


def update_task():
    """
    Update title and/or description of an existing task.

    Prompts user for task ID, validates existence, allows updating
    title and description while preserving ID and status.

    User Story: US3 (Priority P3) - Update Task Details
    """
    print(f"\n{color(BOX_CORNER_TOP_LEFT, MAGENTA)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, MAGENTA)}")
    print(f"{color(BOX_VERTICAL, MAGENTA)}  {ICON_EDIT} {bold(color('UPDATE TASK', BRIGHT_MAGENTA)):<49} {color(BOX_VERTICAL, MAGENTA)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, MAGENTA)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, MAGENTA)}")

    # Get task ID
    try:
        task_id = int(input(f"\n  {color(ICON_BULLET, YELLOW)} {color('Enter task ID to update:', WHITE)} "))
    except ValueError:
        print(error_msg("Please enter a valid number"))
        return

    # Find task
    task = find_task(task_id)
    if not task:
        return

    # Display current task
    print(f"\n  {color(ICON_INFO, BLUE)} {color('Current Details:', BRIGHT_CYAN)}")
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('Title:', BRIGHT_CYAN)} {task['title']}")
    desc = task['description'] if task['description'] else color('[No description]', DIM)
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('Description:', BRIGHT_CYAN)} {desc}")
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('Status:', BRIGHT_CYAN)} {status_badge(task['status'])}")

    # Get and validate new title
    while True:
        title_input = input(f"\n  {color(ICON_BULLET, YELLOW)} {color('Enter new title (or press Enter to keep current):', WHITE)} ").strip()

        # If empty, keep current title
        if not title_input:
            new_title = task['title']
            break

        validated_title, warning = validate_title(title_input)

        if validated_title is None:
            print(error_msg(warning))
            continue

        if warning:
            print(warn_msg(warning))

        new_title = validated_title
        break

    # Get and validate new description
    description_input = input(f"  {color(ICON_BULLET, YELLOW)} {color('Enter new description (or press Enter to keep current):', WHITE)} ")

    # If empty, keep current description
    if not description_input:
        new_description = task['description']
    else:
        validated_description, warning = validate_description(description_input)
        if warning:
            print(warn_msg(warning))
        new_description = validated_description

    # Update task (preserving ID and status)
    task['title'] = new_title
    task['description'] = new_description

    # Confirmation
    print(f"\n  {color(ICON_SUCCESS, GREEN)} {color('Task updated successfully!', BRIGHT_GREEN)}")
    print(f"  {color(ICON_TODO, CYAN)} {color('ID:', BRIGHT_CYAN)} {color(str(task_id), BRIGHT_YELLOW)}")
    print(f"  {color(ICON_EDIT, CYAN)} {color('New Title:', BRIGHT_CYAN)} {task['title']}")
    new_desc = task['description'] if task['description'] else color('[No description]', DIM)
    print(f"  {color(ICON_VIEW, CYAN)} {color('New Description:', BRIGHT_CYAN)} {new_desc}")


def delete_task():
    """
    Delete a task by ID.

    Prompts user for task ID, validates existence, removes task from memory,
    and displays confirmation. Deleted IDs are never reused.

    User Story: US4 (Priority P4) - Delete Task
    """
    print(f"\n{color(BOX_CORNER_TOP_LEFT, RED)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, RED)}")
    print(f"{color(BOX_VERTICAL, RED)}  {ICON_DELETE} {bold(color('DELETE TASK', BRIGHT_RED)):<48} {color(BOX_VERTICAL, RED)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, RED)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, RED)}")

    # Get task ID
    try:
        task_id = int(input(f"\n  {color(ICON_BULLET, YELLOW)} {color('Enter task ID to delete:', WHITE)} "))
    except ValueError:
        print(error_msg("Please enter a valid number"))
        return

    # Find task
    task = find_task(task_id)
    if not task:
        return

    # Display task to be deleted
    print(f"\n  {color(ICON_WARN, YELLOW)} {color('Task to be deleted:', BRIGHT_YELLOW)}")
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('ID:', BRIGHT_CYAN)} {color(str(task['id']), BRIGHT_YELLOW)}")
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('Title:', BRIGHT_CYAN)} {task['title']}")
    print(f"  {color(BOX_VERTICAL, CYAN)} {color('Status:', BRIGHT_CYAN)} {status_badge(task['status'])}")

    # Delete task
    del task_store[task_id]

    # Confirmation
    print(f"\n  {color(ICON_SUCCESS, GREEN)} {color('Task deleted successfully!', BRIGHT_GREEN)}")
    print(f"  {color(ICON_DELETE, CYAN)} {color('Deleted Task ID:', BRIGHT_CYAN)} {color(str(task_id), BRIGHT_YELLOW)}")


def toggle_task_status():
    """
    Toggle task status between "Pending" and "Completed".

    Prompts user for task ID, validates existence, toggles status,
    and displays confirmation. Operation is idempotent.

    User Story: US5 (Priority P5) - Mark Task Complete/Incomplete
    """
    print(f"\n{color(BOX_CORNER_TOP_LEFT, YELLOW)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, YELLOW)}")
    print(f"{color(BOX_VERTICAL, YELLOW)}  {ICON_TOGGLE} {bold(color('MARK COMPLETE/INCOMPLETE', BRIGHT_YELLOW)):<41} {color(BOX_VERTICAL, YELLOW)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, YELLOW)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, YELLOW)}")

    # Get task ID
    try:
        task_id = int(input(f"\n  {color(ICON_BULLET, YELLOW)} {color('Enter task ID:', WHITE)} "))
    except ValueError:
        print(error_msg("Please enter a valid number"))
        return

    # Find task
    task = find_task(task_id)
    if not task:
        return

    # Display current status with visual indicator
    current = status_badge(task['status'])
    print(f"\n  {color(ICON_INFO, BLUE)} {color('Current Status:', BRIGHT_CYAN)} {current}")

    # Toggle status
    if task['status'] == "Pending":
        task['status'] = "Completed"
        new_status_icon = ICON_COMPLETED
        new_status_text = color('Completed', GREEN)
    else:
        task['status'] = "Pending"
        new_status_icon = ICON_PENDING
        new_status_text = color('Pending', BRIGHT_BLUE)

    # Confirmation
    print(f"\n  {color(ICON_SUCCESS, GREEN)} {color('Status updated!', BRIGHT_GREEN)}")
    print(f"  {color(ICON_TODO, CYAN)} {color('Task ID:', BRIGHT_CYAN)} {color(str(task_id), BRIGHT_YELLOW)}")
    print(f"  {new_status_icon} {color('New Status:', BRIGHT_CYAN)} {new_status_text}")


def main():
    """
    Main application entry point and menu loop.

    Displays menu, handles user choice, dispatches to appropriate function,
    and continues until user chooses to exit.
    """
    # Welcome banner
    print(f"\n{color(BOX_CORNER_TOP_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {ICON_HOME} {bold(color('Welcome to', BRIGHT_CYAN)):<38} {color(ICON_TODO, BRIGHT_YELLOW)} {color('Todo App', BRIGHT_YELLOW)} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_T_RIGHT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_T_LEFT, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {color(ICON_INFO, BRIGHT_BLUE)} {color('Your tasks are stored in memory and', DIM):<43} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_VERTICAL, CYAN)}  {color(ICON_WARN, YELLOW)} {color('will be lost when you exit.', DIM):<43} {color(BOX_VERTICAL, CYAN)}")
    print(f"{color(BOX_CORNER_BOTTOM_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, CYAN)}")

    while True:
        display_menu()

        choice = input(f"\n  {color(ICON_ARROW_RIGHT, BRIGHT_GREEN)} {color('Enter your choice (1-6):', WHITE)} ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            toggle_task_status()
        elif choice == "6":
            print(f"\n{color(BOX_CORNER_TOP_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_TOP_RIGHT, CYAN)}")
            print(f"{color(BOX_VERTICAL, CYAN)}  {color(ICON_SUCCESS, GREEN)} {color('Thank you for using the Todo App!', BRIGHT_GREEN):<38} {color(BOX_VERTICAL, CYAN)}")
            print(f"{color(BOX_VERTICAL, CYAN)}  {color(ICON_INFO, BLUE)} {color('All tasks have been cleared from memory.', DIM):<43} {color(BOX_VERTICAL, CYAN)}")
            print(f"{color(BOX_VERTICAL, CYAN)}  {color(ICON_EXIT, BRIGHT_YELLOW)} {color('Goodbye!', BRIGHT_WHITE):<43} {color(BOX_VERTICAL, CYAN)}")
            print(f"{color(BOX_CORNER_BOTTOM_LEFT, CYAN)}{BOX_HORIZONTAL * 56}{color(BOX_CORNER_BOTTOM_RIGHT, CYAN)}\n")
            break
        else:
            print(error_msg("Invalid choice. Please enter a number between 1 and 6."))


if __name__ == "__main__":
    main()
