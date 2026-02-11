"""
Message service for managing chat messages.
Handles CRUD operations for message entities.
"""
from typing import List, Dict, Any
from datetime import datetime
from sqlmodel import Session, select
from models.message import Message, MessageRole

class MessageService:
    """Service for message management operations."""

    def __init__(self, session: Session):
        """
        Initialize message service.

        Args:
            session: Database session
        """
        self.session = session

    async def store_message(
        self,
        conversation_id: int,
        user_id: str,
        role: MessageRole,
        content: str
    ) -> Message:
        """
        Store a new message in the conversation.

        Args:
            conversation_id: Conversation ID
            user_id: User ID
            role: Message role (user/assistant/system)
            content: Message content

        Returns:
            Created message instance
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    async def get_conversation_history(
        self,
        conversation_id: int,
        limit: int = 50
    ) -> List[Message]:
        """
        Get conversation message history.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to return (default 50)

        Returns:
            List of messages ordered chronologically
        """
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(self.session.exec(query).all())

    async def build_message_array(
        self,
        conversation_id: int,
        new_message: str,
        system_prompt: str
    ) -> List[Dict[str, str]]:
        """
        Build message array for agent processing.

        Args:
            conversation_id: Conversation ID
            new_message: New user message
            system_prompt: System prompt for agent

        Returns:
            List of message dicts in OpenAI format
        """
        # Get conversation history
        history = await self.get_conversation_history(conversation_id)

        # Build message array
        messages = [{"role": "system", "content": system_prompt}]

        # Add history
        for msg in history:
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })

        # Add new message
        messages.append({
            "role": "user",
            "content": new_message
        })

        return messages

    async def get_message_count(self, conversation_id: int) -> int:
        """
        Get total message count for a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            Number of messages
        """
        query = select(Message).where(Message.conversation_id == conversation_id)
        messages = self.session.exec(query).all()
        return len(list(messages))

    async def delete_conversation_messages(self, conversation_id: int) -> int:
        """
        Delete all messages in a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            Number of messages deleted
        """
        query = select(Message).where(Message.conversation_id == conversation_id)
        messages = self.session.exec(query).all()
        count = len(list(messages))

        for message in messages:
            self.session.delete(message)

        self.session.commit()
        return count
