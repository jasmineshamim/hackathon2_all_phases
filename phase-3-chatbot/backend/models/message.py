"""
Message model for AI chatbot feature.
Represents a single message in a conversation (from user or assistant).
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    """Message sender role."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    """
    Message entity representing a single message in a conversation.

    Attributes:
        id: Unique message identifier
        conversation_id: Parent conversation (foreign key)
        user_id: Message owner for audit (foreign key to users table)
        role: Message sender role (user/assistant/system)
        content: Message text content
        created_at: When message was sent
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    role: MessageRole = Field(sa_column_kwargs={"nullable": False})
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    # conversation: Optional["Conversation"] = Relationship(back_populates="messages")
