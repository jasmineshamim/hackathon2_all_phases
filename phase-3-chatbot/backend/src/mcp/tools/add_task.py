"""
MCP Tool: add_task
Creates a new task for the user.
"""
from typing import Dict, Any
from sqlmodel import Session, select
from datetime import datetime

async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: Authenticated user's ID
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        dict: {task_id: int, status: str, title: str}

    Raises:
        ValueError: If parameters are invalid
    """
    # Import here to avoid circular dependencies
    from models import Task
    from database import get_session

    # Validate inputs
    if not title or len(title) > 200:
        raise ValueError("Title must be between 1 and 200 characters")

    if description and len(description) > 1000:
        raise ValueError("Description must be max 1000 characters")

    # Create task
    try:
        session = next(get_session())
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }
    except Exception as e:
        session.rollback()
        raise Exception(f"Failed to create task: {str(e)}")
    finally:
        session.close()
