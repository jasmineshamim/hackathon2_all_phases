"""
MCP Tool: update_task
Modifies task title or description.
"""
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime

async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Modify task title or description.

    Args:
        user_id: Authenticated user's ID
        task_id: ID of the task to update
        title: New task title (optional, 1-200 characters)
        description: New task description (optional, max 1000 characters)

    Returns:
        dict: {task_id: int, status: str, title: str, description: str}

    Raises:
        ValueError: If task not found, doesn't belong to user, or parameters invalid
    """
    # Import here to avoid circular dependencies
    from models import Task
    from database import get_session

    # Validate at least one field is being updated
    if title is None and description is None:
        raise ValueError("At least one of title or description must be provided")

    # Validate title length
    if title is not None and (len(title) == 0 or len(title) > 200):
        raise ValueError("Title must be between 1 and 200 characters")

    # Validate description length
    if description is not None and len(description) > 1000:
        raise ValueError("Description must be max 1000 characters")

    try:
        session = next(get_session())

        # Find task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found or doesn't belong to user")

        # Update fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "description": task.description
        }
    except ValueError as e:
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to update task: {str(e)}")
    finally:
        session.close()
