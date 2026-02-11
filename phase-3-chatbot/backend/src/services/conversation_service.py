"""
Conversation service for managing chat conversations.
Handles CRUD operations for conversation entities.
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import Session, select
from models.conversation import Conversation

class ConversationService:
    """Service for conversation management operations."""

    def __init__(self, session: Session):
        """
        Initialize conversation service.

        Args:
            session: Database session
        """
        self.session = session

    async def get_or_create_conversation(
        self,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create new one.

        Args:
            user_id: User ID
            conversation_id: Optional conversation ID to retrieve

        Returns:
            Conversation instance

        Raises:
            ValueError: If conversation_id provided but not found
        """
        if conversation_id:
            # Try to get existing conversation
            query = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = self.session.exec(query).first()

            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found for user {user_id}")

            return conversation
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
            return conversation

    async def update_conversation_timestamp(self, conversation_id: int) -> None:
        """
        Update conversation's updated_at timestamp.

        Args:
            conversation_id: Conversation ID
        """
        query = select(Conversation).where(Conversation.id == conversation_id)
        conversation = self.session.exec(query).first()

        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()

    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[Conversation]:
        """
        Get user's conversations ordered by most recent.

        Args:
            user_id: User ID
            limit: Maximum number of conversations to return

        Returns:
            List of conversations
        """
        query = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(self.session.exec(query).all())

    async def delete_conversation(self, conversation_id: int, user_id: str) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id: Conversation ID
            user_id: User ID for authorization

        Returns:
            True if deleted, False if not found
        """
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = self.session.exec(query).first()

        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True

        return False
