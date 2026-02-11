"""Conversation service for managing chat conversations and messages."""
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from database.models.conversation import Conversation
from database.models.message import Message, MessageRole
from backend.src.utils.errors import ResourceNotFoundError, ValidationError
from datetime import datetime
import uuid


class ConversationService:
    """Service for managing conversations and messages."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(
        self,
        user_id: uuid.UUID,
        title: Optional[str] = None
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=title
        )

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID
    ) -> Conversation:
        """Get a specific conversation by ID."""
        conversation = self.session.get(Conversation, conversation_id)

        if not conversation:
            raise ResourceNotFoundError("Conversation", conversation_id)

        if conversation.user_id != user_id:
            raise ResourceNotFoundError("Conversation", conversation_id)

        return conversation

    def get_conversations(
        self,
        user_id: uuid.UUID,
        limit: int = 20,
        offset: int = 0
    ) -> List[Conversation]:
        """Get all conversations for a user."""
        query = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(
            Conversation.updated_at.desc()
        ).offset(offset).limit(limit)

        conversations = self.session.exec(query).all()
        return list(conversations)

    def add_message(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """Add a message to a conversation."""
        # Verify conversation belongs to user
        conversation = self.get_conversation(user_id, conversation_id)

        if not content or len(content) < 1 or len(content) > 10000:
            raise ValidationError("Content must be between 1 and 10000 characters")

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata
        )

        self.session.add(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)

        self.session.commit()
        self.session.refresh(message)
        return message

    def get_conversation_messages(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """Get messages for a conversation."""
        # Verify conversation belongs to user
        self.get_conversation(user_id, conversation_id)

        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(
            Message.timestamp.asc()
        ).offset(offset).limit(limit)

        messages = self.session.exec(query).all()
        return list(messages)

    def get_conversation_history(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID
    ) -> List[Dict[str, str]]:
        """Get conversation history formatted for AI agent."""
        messages = self.get_conversation_messages(user_id, conversation_id)

        return [
            {
                "role": message.role.value,
                "content": message.content
            }
            for message in messages
        ]

    def delete_conversation(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID
    ) -> uuid.UUID:
        """Delete a conversation and all its messages."""
        conversation = self.get_conversation(user_id, conversation_id)

        # Delete all messages first
        messages_query = select(Message).where(
            Message.conversation_id == conversation_id
        )
        messages = self.session.exec(messages_query).all()
        for message in messages:
            self.session.delete(message)

        # Delete conversation
        self.session.delete(conversation)
        self.session.commit()

        return conversation_id

    def update_conversation_title(
        self,
        user_id: uuid.UUID,
        conversation_id: uuid.UUID,
        title: str
    ) -> Conversation:
        """Update conversation title."""
        conversation = self.get_conversation(user_id, conversation_id)

        if len(title) > 200:
            raise ValidationError("Title must not exceed 200 characters")

        conversation.title = title
        conversation.updated_at = datetime.utcnow()

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation
