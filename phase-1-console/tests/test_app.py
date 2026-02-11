"""
Automated testing script for Todo Console Application.
Simulates user interactions to validate all core features.
"""

import sys
import io
from contextlib import redirect_stdout

# Import the todo app
sys.path.insert(0, 'src')
import todo_app

def test_scenario(name, description, inputs, expected_outputs):
    """
    Run a test scenario with simulated inputs.

    Args:
        name: Test scenario name
        description: What the test validates
        inputs: List of input strings to simulate
        expected_outputs: List of expected output strings
    """
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"Description: {description}")
    print(f"{'='*70}")

    # Reset the app state
    todo_app.task_store = {}
    todo_app.next_task_id = 1

    # Prepare simulated input
    input_text = '\n'.join(inputs) + '\n'

    # Capture output
    captured_output = io.StringIO()

    try:
        # Simulate stdin
        sys.stdin = io.StringIO(input_text)

        # Redirect stdout to capture output
        with redirect_stdout(captured_output):
            # Run main (will exit when '6' is entered)
            try:
                todo_app.main()
            except SystemExit:
                pass

        output = captured_output.getvalue()

        # Check for expected outputs
        passed = all(expected in output for expected in expected_outputs)

        if passed:
            print("[PASS]")
            # Print key outputs
            print("\nKey Outputs:")
            for expected in expected_outputs:
                if expected in output:
                    print(f"  [OK] Found: '{expected}'")
        else:
            print("[FAIL]")
            print("\nExpected outputs not found:")
            for expected in expected_outputs:
                if expected not in output:
                    print(f"  [X] Missing: '{expected}'")
            print(f"\nActual output:\n{output}")

        return passed

    finally:
        # Restore stdin
        sys.stdin = sys.__stdin__

def run_tests():
    """Run all test scenarios."""
    print("\n" + "="*70)
    print("AUTOMATED TODO APP TESTING")
    print("="*70)

    results = []

    # Test 1: Add Task - Happy Path
    results.append(test_scenario(
        "Scenario 1: Add Task - Happy Path",
        "Create a task with title and description",
        [
            '1',  # Add Task
            'Buy groceries',  # Title
            'Milk, eggs, bread',  # Description
            '6'  # Exit
        ],
        [
            'Success! Task created with ID 1',
            'Title: Buy groceries',
            'Status: Pending'
        ]
    ))

    # Test 2: Add Task - Empty Description
    results.append(test_scenario(
        "Scenario 2: Add Task - Empty Description",
        "Create a task without description",
        [
            '1',  # Add Task
            'Quick reminder',  # Title
            '',  # Empty description
            '6'  # Exit
        ],
        [
            'Success! Task created with ID 1',
            'Title: Quick reminder'
        ]
    ))

    # Test 3: Add Task - Empty Title (Error)
    results.append(test_scenario(
        "Scenario 3: Add Task - Empty Title",
        "Validate that empty title is rejected",
        [
            '1',  # Add Task
            '',  # Empty title
            'Valid Title',  # Valid title after error
            'Some description',
            '6'  # Exit
        ],
        [
            'Error: Title cannot be empty',
            'Success! Task created with ID 1',
            'Title: Valid Title'
        ]
    ))

    # Test 4: View Tasks - Multiple Tasks
    results.append(test_scenario(
        "Scenario 4: View Tasks - Multiple Tasks",
        "Add multiple tasks and view them",
        [
            '1', 'Task One', 'Description 1',  # Add task 1
            '1', 'Task Two', 'Description 2',  # Add task 2
            '1', 'Task Three', '',  # Add task 3 (no description)
            '2',  # View Tasks
            '6'  # Exit
        ],
        [
            'ID: 1',
            'Title: Task One',
            'Description: Description 1',
            'ID: 2',
            'Title: Task Two',
            'ID: 3',
            'Title: Task Three',
            '[No description]',
            'Total tasks: 3'
        ]
    ))

    # Test 5: View Tasks - Empty List
    results.append(test_scenario(
        "Scenario 5: View Tasks - Empty List",
        "View tasks when none exist",
        [
            '2',  # View Tasks
            '6'  # Exit
        ],
        [
            'No tasks found. Add your first task to get started!'
        ]
    ))

    # Test 6: Update Task
    results.append(test_scenario(
        "Scenario 6: Update Task",
        "Modify task title and description",
        [
            '1', 'Finsih report', 'By Friday',  # Add task with typo
            '3',  # Update Task
            '1',  # Task ID 1
            'Finish report',  # New title
            'By Friday EOD',  # New description
            '2',  # View to verify
            '6'  # Exit
        ],
        [
            'Success! Task ID 1 updated',
            'New title: Finish report',
            'New description: By Friday EOD'
        ]
    ))

    # Test 7: Update Task - Invalid ID
    results.append(test_scenario(
        "Scenario 7: Update Task - Invalid ID",
        "Try to update non-existent task",
        [
            '3',  # Update Task
            '99',  # Non-existent ID
            '6'  # Exit
        ],
        [
            'Task ID 99 not found'
        ]
    ))

    # Test 8: Delete Task
    results.append(test_scenario(
        "Scenario 8: Delete Task",
        "Remove a task from the list",
        [
            '1', 'Task 1', 'Desc 1',
            '1', 'Task 2', 'Desc 2',
            '1', 'Task 3', 'Desc 3',
            '4',  # Delete Task
            '2',  # Task ID 2
            '2',  # View Tasks
            '6'  # Exit
        ],
        [
            'Task ID 2 deleted successfully',
            'ID: 1',
            'ID: 3',
            'Total tasks: 2'
        ]
    ))

    # Test 9: Delete Task - Invalid ID
    results.append(test_scenario(
        "Scenario 9: Delete Task - Invalid ID",
        "Try to delete non-existent task",
        [
            '4',  # Delete Task
            '99',  # Non-existent ID
            '6'  # Exit
        ],
        [
            'Task ID 99 not found'
        ]
    ))

    # Test 10: Toggle Status - Mark Complete
    results.append(test_scenario(
        "Scenario 10: Toggle Status - Mark Complete",
        "Mark a pending task as completed",
        [
            '1', 'Test Task', 'Test Description',
            '5',  # Toggle Status
            '1',  # Task ID 1
            '2',  # View to verify
            '6'  # Exit
        ],
        [
            'Task ID 1 marked as Completed',
            'Status: Completed'
        ]
    ))

    # Test 11: Toggle Status - Mark Incomplete
    results.append(test_scenario(
        "Scenario 11: Toggle Status - Mark Incomplete",
        "Mark a completed task as pending",
        [
            '1', 'Test Task', 'Test Description',
            '5', '1',  # Mark complete
            '5', '1',  # Mark incomplete
            '2',  # View to verify
            '6'  # Exit
        ],
        [
            'Task ID 1 marked as Completed',
            'Task ID 1 marked as Pending',
            'Status: Pending'
        ]
    ))

    # Test 12: Toggle Status - Invalid ID
    results.append(test_scenario(
        "Scenario 12: Toggle Status - Invalid ID",
        "Try to toggle status of non-existent task",
        [
            '5',  # Toggle Status
            '99',  # Non-existent ID
            '6'  # Exit
        ],
        [
            'Task ID 99 not found'
        ]
    ))

    # Test 13: Invalid Menu Choice
    results.append(test_scenario(
        "Scenario 13: Invalid Menu Choice",
        "Enter invalid menu option",
        [
            'abc',  # Invalid choice
            '99',  # Invalid choice
            '6'  # Exit
        ],
        [
            'Error: Invalid choice. Please try again.',
            'Please enter a number between 1 and 6.'
        ]
    ))

    # Test 14: Full Workflow
    results.append(test_scenario(
        "Scenario 14: Full Workflow",
        "Complete add-view-update-toggle-delete workflow",
        [
            '1', 'Complete project', 'Due next week',  # Add
            '2',  # View
            '3', '1', 'Complete project report', 'Due next Friday',  # Update
            '5', '1',  # Mark complete
            '4', '1',  # Delete
            '2',  # View (should be empty)
            '6'  # Exit
        ],
        [
            'Success! Task created with ID 1',
            'ID: 1',
            'Success! Task ID 1 updated',
            'Task ID 1 marked as Completed',
            'Task ID 1 deleted successfully',
            'No tasks found'
        ]
    ))

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    if failed == 0:
        print("\nALL TESTS PASSED! Application is working correctly.")
    else:
        print(f"\n{failed} test(s) failed. Review output above for details.")

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
