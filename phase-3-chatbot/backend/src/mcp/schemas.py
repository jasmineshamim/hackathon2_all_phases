"""
MCP tool schemas for task management operations.
Defines input/output schemas for all task-related tools.
"""
from typing import Optional, List
from pydantic import BaseModel, Field

# Tool Input Schemas

class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""
    user_id: str = Field(description="Authenticated user's ID")
    title: str = Field(description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Optional task description", max_length=1000)

class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""
    user_id: str = Field(description="Authenticated user's ID")
    status: Optional[str] = Field("all", description="Filter by status: all, pending, completed")

class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool."""
    user_id: str = Field(description="Authenticated user's ID")
    task_id: int = Field(description="ID of the task to mark as complete")

class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool."""
    user_id: str = Field(description="Authenticated user's ID")
    task_id: int = Field(description="ID of the task to delete")

class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""
    user_id: str = Field(description="Authenticated user's ID")
    task_id: int = Field(description="ID of the task to update")
    title: Optional[str] = Field(None, description="New task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="New task description", max_length=1000)

# Tool Output Schemas

class TaskOutput(BaseModel):
    """Output schema for task operations."""
    task_id: int
    status: str
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskListOutput(BaseModel):
    """Output schema for list_tasks tool."""
    tasks: List[dict]
    count: int

class ToolError(BaseModel):
    """Error schema for tool operations."""
    error: str
    message: str
    details: Optional[dict] = None

# JSON Schemas for OpenAI Agents SDK

ADD_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user's ID"},
                "title": {"type": "string", "description": "Task title (1-200 characters)"},
                "description": {"type": "string", "description": "Optional task description (max 1000 characters)"}
            },
            "required": ["user_id", "title"]
        }
    }
}

LIST_TASKS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Retrieve tasks from the user's list",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user's ID"},
                "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status"}
            },
            "required": ["user_id"]
        }
    }
}

COMPLETE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a task as complete",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user's ID"},
                "task_id": {"type": "integer", "description": "ID of the task to complete"}
            },
            "required": ["user_id", "task_id"]
        }
    }
}

DELETE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Remove a task from the user's list",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user's ID"},
                "task_id": {"type": "integer", "description": "ID of the task to delete"}
            },
            "required": ["user_id", "task_id"]
        }
    }
}

UPDATE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Modify task title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Authenticated user's ID"},
                "task_id": {"type": "integer", "description": "ID of the task to update"},
                "title": {"type": "string", "description": "New task title (optional)"},
                "description": {"type": "string", "description": "New task description (optional)"}
            },
            "required": ["user_id", "task_id"]
        }
    }
}
