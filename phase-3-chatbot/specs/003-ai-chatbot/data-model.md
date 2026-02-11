# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the data entities and relationships for the AI chatbot feature. The design extends the existing Phase II schema (users, tasks) with new entities for conversation management.

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
│  (Phase II)     │
│─────────────────│
│ id (PK)         │
│ email           │
│ name            │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼──────────────┐   ┌──────▼──────────┐
│  conversations   │   │     tasks       │
│                  │   │   (Phase II)    │
│──────────────────│   │─────────────────│
│ id (PK)          │   │ id (PK)         │
│ user_id (FK)     │   │ user_id (FK)    │
│ created_at       │   │ title           │
│ updated_at       │   │ description     │
└────────┬─────────┘   │ completed       │
         │             │ created_at      │
         │ 1:N         │ updated_at      │
         │             └─────────────────┘
    ┌────▼─────────────┐
    │    messages      │
    │──────────────────│
    │ id (PK)          │
    │ conversation_id  │
    │   (FK)           │
    │ user_id (FK)     │
    │ role             │
    │ content          │
    │ created_at       │
    └──────────────────┘
```

## Entities

### 1. Conversation

**Purpose**: Represents a chat session between a user and the AI assistant.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique conversation identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users.id | Owner of the conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When conversation started |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Relationships**:
- **Belongs to**: User (1:1) - Each conversation belongs to one user
- **Has many**: Messages (1:N) - Each conversation contains multiple messages

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` for fast user conversation lookup
- INDEX on `updated_at` for sorting by recent activity

**Business Rules**:
- User can have multiple conversations (unlimited)
- Conversation is automatically created on first chat message
- Deleting conversation cascades to delete all messages
- `updated_at` is updated whenever a new message is added

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

---

### 2. Message

**Purpose**: Represents a single message in a conversation (from user or assistant).

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique message identifier |
| conversation_id | INTEGER | NOT NULL, FOREIGN KEY → conversations.id | Parent conversation |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users.id | Message owner (for audit) |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant', 'system') | Message sender role |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was sent |

**Relationships**:
- **Belongs to**: Conversation (N:1) - Each message belongs to one conversation
- **Belongs to**: User (N:1) - Each message is associated with a user

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id` for fast conversation history retrieval
- INDEX on `created_at` for chronological ordering
- INDEX on `user_id` for user message history

**Business Rules**:
- Messages are immutable (no updates after creation)
- Role must be one of: 'user', 'assistant', 'system'
- Content length limited to 10,000 characters
- Messages are ordered chronologically by `created_at`
- Deleting conversation cascades to delete all messages

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: MessageRole = Field(sa_column_kwargs={"nullable": False})
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

---

### 3. Task (Existing - Phase II)

**Purpose**: Represents a todo item in the user's task list.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users.id | Task owner |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When task was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification time |

**Note**: This entity exists from Phase II. No modifications needed for Phase III.

---

### 4. User (Existing - Phase II)

**Purpose**: Represents an authenticated user account.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | NOT NULL, UNIQUE | User email address |
| name | VARCHAR(255) | NOT NULL | User display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |

**Note**: This entity exists from Phase II (managed by Better Auth). No modifications needed for Phase III.

---

## Database Migration

### Migration Script: 003_add_conversation_tables.sql

```sql
-- Create conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_conversations_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Create indexes for conversations
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);

-- Create messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_messages_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_messages_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Create indexes for messages
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Add comment for documentation
COMMENT ON TABLE conversations IS 'Chat sessions between users and AI assistant';
COMMENT ON TABLE messages IS 'Individual messages within conversations';
```

### Alembic Migration (Python)

```python
# backend/src/db/migrations/versions/003_add_conversation_tables.py
"""Add conversation and message tables

Revision ID: 003
Revises: 002
Create Date: 2026-02-08
"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.CheckConstraint("role IN ('user', 'assistant', 'system')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_user_id', 'messages', ['user_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

---

## Data Access Patterns

### Common Queries

**1. Get or Create Conversation**
```sql
-- Check if conversation exists
SELECT id, user_id, created_at, updated_at
FROM conversations
WHERE id = ? AND user_id = ?;

-- Create new conversation if not exists
INSERT INTO conversations (user_id, created_at, updated_at)
VALUES (?, NOW(), NOW())
RETURNING id, user_id, created_at, updated_at;
```

**2. Fetch Conversation History**
```sql
-- Get last 50 messages for a conversation
SELECT id, conversation_id, user_id, role, content, created_at
FROM messages
WHERE conversation_id = ?
ORDER BY created_at ASC
LIMIT 50;
```

**3. Store User Message**
```sql
INSERT INTO messages (conversation_id, user_id, role, content, created_at)
VALUES (?, ?, 'user', ?, NOW())
RETURNING id, conversation_id, user_id, role, content, created_at;
```

**4. Store Assistant Message**
```sql
INSERT INTO messages (conversation_id, user_id, role, content, created_at)
VALUES (?, ?, 'assistant', ?, NOW())
RETURNING id, conversation_id, user_id, role, content, created_at;
```

**5. Update Conversation Timestamp**
```sql
UPDATE conversations
SET updated_at = NOW()
WHERE id = ?;
```

**6. List User Conversations**
```sql
SELECT c.id, c.user_id, c.created_at, c.updated_at,
       (SELECT content FROM messages WHERE conversation_id = c.id ORDER BY created_at DESC LIMIT 1) as last_message
FROM conversations c
WHERE c.user_id = ?
ORDER BY c.updated_at DESC
LIMIT 20;
```

---

## Performance Considerations

### Indexing Strategy
- **conversations.user_id**: Fast lookup of user's conversations
- **conversations.updated_at**: Sort conversations by recent activity
- **messages.conversation_id**: Fast retrieval of conversation history
- **messages.created_at**: Chronological ordering of messages
- **messages.user_id**: Audit trail and user message history

### Query Optimization
- Limit conversation history to last 50 messages (pagination for older messages)
- Use connection pooling for concurrent requests
- Consider read replicas for high-traffic scenarios (future optimization)

### Storage Estimates
- Average message size: ~200 characters = ~200 bytes
- 1000 users × 100 messages each = 100,000 messages = ~20 MB
- Indexes add ~30% overhead = ~26 MB total
- Very manageable for Neon PostgreSQL free tier

---

## Data Retention Policy

### Current Policy (MVP)
- Conversations: Retained indefinitely
- Messages: Retained indefinitely
- No automatic archival or deletion

### Future Considerations
- Archive conversations older than 6 months
- Implement soft delete for user-requested deletions
- GDPR compliance: Allow users to export/delete their data

---

## Validation Rules

### Conversation
- `user_id` must exist in users table
- `created_at` and `updated_at` must be valid timestamps
- `updated_at` >= `created_at`

### Message
- `conversation_id` must exist in conversations table
- `user_id` must match conversation.user_id
- `role` must be one of: 'user', 'assistant', 'system'
- `content` length: 1-10,000 characters
- `created_at` must be valid timestamp

---

## Security Considerations

### Data Access Control
- All queries must filter by authenticated user_id
- No cross-user data access allowed
- Conversation and message access requires user ownership verification

### Data Privacy
- Message content is not encrypted at rest (relies on database encryption)
- No PII should be stored in message content beyond what user provides
- Conversation data is user-scoped and isolated

---

## Testing Data

### Sample Conversation
```json
{
  "conversation": {
    "id": 1,
    "user_id": "user_123",
    "created_at": "2026-02-08T10:00:00Z",
    "updated_at": "2026-02-08T10:05:00Z"
  },
  "messages": [
    {
      "id": 1,
      "conversation_id": 1,
      "user_id": "user_123",
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-02-08T10:00:00Z"
    },
    {
      "id": 2,
      "conversation_id": 1,
      "user_id": "user_123",
      "role": "assistant",
      "content": "I've added 'Buy groceries' to your task list.",
      "created_at": "2026-02-08T10:00:02Z"
    },
    {
      "id": 3,
      "conversation_id": 1,
      "user_id": "user_123",
      "role": "user",
      "content": "Show me my tasks",
      "created_at": "2026-02-08T10:05:00Z"
    },
    {
      "id": 4,
      "conversation_id": 1,
      "user_id": "user_123",
      "role": "assistant",
      "content": "Here are your tasks:\n1. Buy groceries (pending)",
      "created_at": "2026-02-08T10:05:01Z"
    }
  ]
}
```

---

## Next Steps

1. ✅ Data model defined
2. ⏭️ Create API contracts (chat-api.yaml, mcp-tools.yaml)
3. ⏭️ Generate quickstart.md
4. ⏭️ Run database migrations
5. ⏭️ Implement SQLModel models in backend
