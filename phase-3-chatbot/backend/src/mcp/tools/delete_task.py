"""
MCP Tool: delete_task
Removes a task from the user's list.
"""
from typing import Dict, Any
from sqlmodel import Session, select

async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Remove a task from the user's list.

    Args:
        user_id: Authenticated user's ID
        task_id: ID of the task to delete

    Returns:
        dict: {task_id: int, status: str, title: str}

    Raises:
        ValueError: If task not found or doesn't belong to user
    """
    # Import here to avoid circular dependencies
    from models import Task
    from database import get_session

    try:
        session = next(get_session())

        # Find task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found or doesn't belong to user")

        # Store title before deletion
        task_title = task.title

        # Delete task
        session.delete(task)
        session.commit()

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task_title
        }
    except ValueError as e:
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to delete task: {str(e)}")
    finally:
        session.close()
