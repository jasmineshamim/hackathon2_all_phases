"""
Conversation model for AI chatbot feature.
Represents a chat session between a user and the AI assistant.
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    """
    Conversation entity representing a chat session.

    Attributes:
        id: Unique conversation identifier
        user_id: Owner of the conversation (foreign key to users table)
        created_at: When conversation started
        updated_at: Last message timestamp
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    # Note: Relationship to Message model will be defined when Message model is created
    # messages: List["Message"] = Relationship(back_populates="conversation")
