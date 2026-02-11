"""
MCP Tool: complete_task
Marks a task as complete.
"""
from typing import Dict, Any
from sqlmodel import Session, select
from datetime import datetime

async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        user_id: Authenticated user's ID
        task_id: ID of the task to mark as complete

    Returns:
        dict: {task_id: int, status: str, title: str, completed: bool}

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

        # Check if already completed
        if task.completed:
            return {
                "task_id": task.id,
                "status": "already_completed",
                "title": task.title,
                "completed": True
            }

        # Mark as complete
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title,
            "completed": True
        }
    except ValueError as e:
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to complete task: {str(e)}")
    finally:
        session.close()
