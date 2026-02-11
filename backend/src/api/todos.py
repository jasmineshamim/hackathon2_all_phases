"""REST API endpoints for todo operations."""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from database.models.base import get_session
from database.models.todo import TodoStatus, TodoPriority
from backend.src.services.todo_service import TodoService
from backend.src.middleware.auth import security, get_current_user_id
from backend.src.utils.errors import format_error_response, APIError

router = APIRouter()


# Request/Response Models
class TodoCreate(BaseModel):
    """Request model for creating a todo."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM)
    due_date: Optional[datetime] = None


class TodoUpdate(BaseModel):
    """Request model for updating a todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    due_date: Optional[datetime] = None


class TodoResponse(BaseModel):
    """Response model for a todo."""
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


@router.get("/statistics", response_model=dict)
async def get_task_statistics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get task statistics for the authenticated user."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        # Get all todos for the user
        all_todos = service.get_todos(
            user_id=uuid.UUID(user_id),
            status=None,
            priority=None,
            limit=1000,
            offset=0
        )

        # Calculate statistics
        total_count = len(all_todos)
        pending_count = sum(1 for todo in all_todos if todo.status == TodoStatus.PENDING)
        completed_count = sum(1 for todo in all_todos if todo.status == TodoStatus.COMPLETED)

        return {
            "total_count": total_count,
            "pending_count": pending_count,
            "completed_count": completed_count
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.get("/", response_model=dict)
async def get_todos(
    status: Optional[TodoStatus] = Query(None),
    priority: Optional[TodoPriority] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get all todos for the authenticated user."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        todos = service.get_todos(
            user_id=uuid.UUID(user_id),
            status=status,
            priority=priority,
            limit=limit,
            offset=offset
        )

        return {
            "success": True,
            "data": {
                "todos": [
                    {
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "status": todo.status.value,
                        "priority": todo.priority.value,
                        "due_date": todo.due_date.isoformat() if todo.due_date else None,
                        "created_at": todo.created_at.isoformat(),
                        "updated_at": todo.updated_at.isoformat()
                    }
                    for todo in todos
                ],
                "total": len(todos)
            },
            "message": "Todos retrieved successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Create a new todo."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        todo = service.create_todo(
            user_id=uuid.UUID(user_id),
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            due_date=todo_data.due_date
        )

        return {
            "success": True,
            "data": {
                "todo": {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "status": todo.status.value,
                    "priority": todo.priority.value,
                    "due_date": todo.due_date.isoformat() if todo.due_date else None,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                }
            },
            "message": "Todo created successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.get("/{todo_id}", response_model=dict)
async def get_todo(
    todo_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        todo = service.get_todo_by_id(
            user_id=uuid.UUID(user_id),
            todo_id=todo_id
        )

        return {
            "success": True,
            "data": {
                "todo": {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "status": todo.status.value,
                    "priority": todo.priority.value,
                    "due_date": todo.due_date.isoformat() if todo.due_date else None,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                }
            },
            "message": "Todo retrieved successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.put("/{todo_id}", response_model=dict)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Update an existing todo."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        todo = service.update_todo(
            user_id=uuid.UUID(user_id),
            todo_id=todo_id,
            title=todo_data.title,
            description=todo_data.description,
            status=todo_data.status,
            priority=todo_data.priority,
            due_date=todo_data.due_date
        )

        return {
            "success": True,
            "data": {
                "todo": {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "status": todo.status.value,
                    "priority": todo.priority.value,
                    "due_date": todo.due_date.isoformat() if todo.due_date else None,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                }
            },
            "message": "Todo updated successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.delete("/{todo_id}", response_model=dict)
async def delete_todo(
    todo_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Delete a todo."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        deleted_id = service.delete_todo(
            user_id=uuid.UUID(user_id),
            todo_id=todo_id
        )

        return {
            "success": True,
            "data": {
                "deleted_id": deleted_id
            },
            "message": "Todo deleted successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.put("/{todo_id}/toggle-status", response_model=dict)
async def toggle_todo_status(
    todo_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Toggle todo status between pending and completed."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        todo = service.toggle_todo_status(
            user_id=uuid.UUID(user_id),
            todo_id=todo_id
        )

        return {
            "success": True,
            "data": {
                "todo": {
                    "id": todo.id,
                    "title": todo.title,
                    "status": todo.status.value
                }
            },
            "message": "Todo status updated successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))
