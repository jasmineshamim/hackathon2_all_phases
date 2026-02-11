"""Conversation model for chat sessions."""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class Conversation(SQLModel, table=True):
    """Conversation model representing a chat session."""

    __tablename__ = "conversations"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    title: Optional[str] = Field(default=None, max_length=200)
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Todo management conversation",
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
