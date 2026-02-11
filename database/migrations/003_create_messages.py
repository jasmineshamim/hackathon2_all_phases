"""Database migration for messages table."""
from sqlmodel import SQLModel
from database.models.base import engine
from database.models.message import Message
from database.models.conversation import Conversation
import logging

logger = logging.getLogger(__name__)


def upgrade():
    """Create messages table with indexes."""
    try:
        logger.info("Creating messages table...")

        # Import models to ensure they're registered
        from database.models.message import Message
        from database.models.conversation import Conversation

        # Create tables
        SQLModel.metadata.create_all(engine, tables=[Message.__table__])

        logger.info("Messages table created successfully")

        # Note: Indexes are automatically created by SQLModel based on Field(index=True)
        # - conversation_id (indexed for conversation-specific queries)
        # - timestamp (indexed for chronological ordering)
        # Composite index on (conversation_id, timestamp) would be ideal for efficient retrieval

    except Exception as e:
        logger.error(f"Failed to create messages table: {str(e)}")
        raise


def downgrade():
    """Drop messages table."""
    try:
        logger.info("Dropping messages table...")
        SQLModel.metadata.drop_all(engine, tables=[Message.__table__])
        logger.info("Messages table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop messages table: {str(e)}")
        raise


if __name__ == "__main__":
    upgrade()
