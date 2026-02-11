"""MCP tools for todo operations."""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from database.models.base import get_session
from database.models.todo import TodoStatus, TodoPriority
from backend.src.services.todo_service import TodoService
from backend.src.middleware.auth import security, get_current_user_id
from backend.src.utils.errors import format_error_response, APIError
from datetime import datetime
import uuid

router = APIRouter()


# MCP Tool Schemas
class MCPToolSchema:
    """Base schema for MCP tool definition."""

    def __init__(self, name: str, description: str, input_schema: dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }


# Define MCP Tools
CREATE_TODO_TOOL = MCPToolSchema(
    name="create-todo",
    description="Creates a new todo item with the specified title and optional details.",
    input_schema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title of the task (required)"
            },
            "description": {
                "type": "string",
                "description": "Detailed description of the task (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "Priority level of the task (optional, default: medium)"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "Due date for the task in ISO 8601 format (optional)"
            }
        },
        "required": ["title"]
    }
)

LIST_TODOS_TOOL = MCPToolSchema(
    name="list-todos",
    description="Retrieves all todo items for the authenticated user, with optional filtering.",
    input_schema={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["pending", "completed"],
                "description": "Filter by status (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "Filter by priority (optional)"
            }
        }
    }
)

UPDATE_TODO_TOOL = MCPToolSchema(
    name="update-todo",
    description="Updates an existing todo item with the specified changes.",
    input_schema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "integer",
                "description": "ID of the todo to update (required)"
            },
            "title": {
                "type": "string",
                "description": "New title for the task (optional)"
            },
            "description": {
                "type": "string",
                "description": "New description for the task (optional)"
            },
            "status": {
                "type": "string",
                "enum": ["pending", "completed"],
                "description": "New status for the task (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "New priority for the task (optional)"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "New due date for the task (optional)"
            }
        },
        "required": ["todo_id"]
    }
)

DELETE_TODO_TOOL = MCPToolSchema(
    name="delete-todo",
    description="Deletes a todo item by ID.",
    input_schema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "integer",
                "description": "ID of the todo to delete (required)"
            }
        },
        "required": ["todo_id"]
    }
)

TOGGLE_TODO_STATUS_TOOL = MCPToolSchema(
    name="toggle-todo-status",
    description="Toggles the status of a todo item between pending and completed.",
    input_schema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "integer",
                "description": "ID of the todo to toggle (required)"
            }
        },
        "required": ["todo_id"]
    }
)

# All available MCP tools
MCP_TOOLS = [
    CREATE_TODO_TOOL,
    LIST_TODOS_TOOL,
    UPDATE_TODO_TOOL,
    DELETE_TODO_TOOL,
    TOGGLE_TODO_STATUS_TOOL
]


@router.get("/tools")
async def discover_mcp_tools():
    """MCP tool discovery endpoint."""
    return {
        "tools": [tool.to_dict() for tool in MCP_TOOLS]
    }


@router.post("/tools/create-todo")
async def create_todo_tool(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """MCP tool: Create a new todo."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        # Parse due_date if provided
        parsed_due_date = None
        if due_date:
            parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        todo = service.create_todo(
            user_id=uuid.UUID(user_id),
            title=title,
            description=description,
            priority=TodoPriority(priority),
            due_date=parsed_due_date
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
        return format_error_response(e)


@router.post("/tools/list-todos")
async def list_todos_tool(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """MCP tool: List all todos."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        # Parse filters
        status_filter = TodoStatus(status) if status else None
        priority_filter = TodoPriority(priority) if priority else None

        todos = service.get_todos(
            user_id=uuid.UUID(user_id),
            status=status_filter,
            priority=priority_filter
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
        return format_error_response(e)


@router.post("/tools/update-todo")
async def update_todo_tool(
    todo_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """MCP tool: Update a todo."""
    try:
        user_id = await get_current_user_id(credentials)
        service = TodoService(session)

        # Parse optional fields
        status_value = TodoStatus(status) if status else None
        priority_value = TodoPriority(priority) if priority else None
        parsed_due_date = None
        if due_date:
            parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

        todo = service.update_todo(
            user_id=uuid.UUID(user_id),
            todo_id=todo_id,
            title=title,
            description=description,
            status=status_value,
            priority=priority_value,
            due_date=parsed_due_date
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
        return format_error_response(e)


@router.post("/tools/delete-todo")
async def delete_todo_tool(
    todo_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """MCP tool: Delete a todo."""
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
        return format_error_response(e)


@router.post("/tools/toggle-todo-status")
async def toggle_todo_status_tool(
    todo_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """MCP tool: Toggle todo status."""
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
        return format_error_response(e)
