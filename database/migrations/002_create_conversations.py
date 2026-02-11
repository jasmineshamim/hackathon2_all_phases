"""Database migration for conversations table."""
from sqlmodel import SQLModel
from database.models.base import engine
from database.models.conversation import Conversation
from database.models.user import User
import logging

logger = logging.getLogger(__name__)


def upgrade():
    """Create conversations table with indexes."""
    try:
        logger.info("Creating conversations table...")

        # Import models to ensure they're registered
        from database.models.conversation import Conversation
        from database.models.user import User

        # Create tables
        SQLModel.metadata.create_all(engine, tables=[Conversation.__table__])

        logger.info("Conversations table created successfully")

        # Note: Indexes are automatically created by SQLModel based on Field(index=True)
        # - user_id (indexed for user-specific queries)
        # - created_at (indexed for chronological ordering)

    except Exception as e:
        logger.error(f"Failed to create conversations table: {str(e)}")
        raise


def downgrade():
    """Drop conversations table."""
    try:
        logger.info("Dropping conversations table...")
        SQLModel.metadata.drop_all(engine, tables=[Conversation.__table__])
        logger.info("Conversations table dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop conversations table: {str(e)}")
        raise


if __name__ == "__main__":
    upgrade()
