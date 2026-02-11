"""Message model for chat messages."""
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message model representing individual chat messages."""

    __tablename__ = "messages"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "user",
                "content": "Add a task to buy groceries",
                "metadata": {"tool_calls": []}
            }
        }
