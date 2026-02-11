"""Todo model for task management."""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class TodoStatus(str, Enum):
    """Todo status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    """Todo priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(SQLModel, table=True):
    """Todo model representing a task item."""

    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TodoStatus = Field(default=TodoStatus.PENDING, nullable=False)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM, nullable=False)
    due_date: Optional[datetime] = Field(default=None)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "pending",
                "priority": "medium",
                "due_date": "2026-02-10T10:00:00Z"
            }
        }
