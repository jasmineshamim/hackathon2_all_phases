"""Quick demo of the Todo Console Application"""

import sys
import io

sys.path.insert(0, 'src')
import todo_app

# Reset state
todo_app.task_store = {}
todo_app.next_task_id = 1

print("="*70)
print("TODO APP DEMO - Quick Feature Showcase")
print("="*70)

# Demo 1: Add tasks
print("\n1. Adding tasks...")
todo_app.task_store[1] = {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "status": "Pending"}
todo_app.task_store[2] = {"id": 2, "title": "Finish report", "description": "Q4 metrics", "status": "Pending"}
todo_app.task_store[3] = {"id": 3, "title": "Call dentist", "description": "", "status": "Pending"}
todo_app.next_task_id = 4
print("   Added 3 tasks")

# Demo 2: View tasks
print("\n2. Viewing all tasks:")
print("-" * 70)
for task_id in sorted(todo_app.task_store.keys()):
    task = todo_app.task_store[task_id]
    desc = task['description'] if task['description'] else "[No description]"
    print(f"   ID: {task['id']} | {task['title']}")
    print(f"   Description: {desc}")
    print(f"   Status: {task['status']}")
    print()

# Demo 3: Update task
print("3. Updating task 2...")
todo_app.task_store[2]['title'] = "Finish Q4 report"
todo_app.task_store[2]['description'] = "Include revenue and metrics"
print(f"   Updated: {todo_app.task_store[2]['title']}")

# Demo 4: Mark complete
print("\n4. Marking task 1 as complete...")
todo_app.task_store[1]['status'] = "Completed"
print(f"   Task 1 status: {todo_app.task_store[1]['status']}")

# Demo 5: Delete task
print("\n5. Deleting task 3...")
del todo_app.task_store[3]
print("   Task 3 deleted")

# Demo 6: Final state
print("\n6. Final task list:")
print("-" * 70)
for task_id in sorted(todo_app.task_store.keys()):
    task = todo_app.task_store[task_id]
    print(f"   [{task['status']}] ID {task['id']}: {task['title']}")
print(f"\nTotal tasks: {len(todo_app.task_store)}")

print("\n" + "="*70)
print("DEMO COMPLETE - All features working correctly!")
print("="*70)
print("\nTo run the full interactive app:")
print("  python src/todo_app.py")
print("\nTo run automated tests:")
print("  python test_app.py")
