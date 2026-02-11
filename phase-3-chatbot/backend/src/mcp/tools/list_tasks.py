"""
MCP Tool: list_tasks
Retrieves tasks from the user's list with optional filtering.
"""
from typing import Dict, Any, List
from sqlmodel import Session, select

async def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    Retrieve tasks from the user's list.

    Args:
        user_id: Authenticated user's ID
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        dict: {tasks: List[dict], count: int}

    Raises:
        ValueError: If status parameter is invalid
    """
    # Import here to avoid circular dependencies
    from models import Task
    from database import get_session

    # Validate status parameter
    valid_statuses = ["all", "pending", "completed"]
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

    try:
        session = next(get_session())

        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Execute query
        results = session.exec(query).all()

        # Format tasks
        tasks = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            for task in results
        ]

        return {
            "tasks": tasks,
            "count": len(tasks)
        }
    except Exception as e:
        raise Exception(f"Failed to list tasks: {str(e)}")
    finally:
        session.close()
