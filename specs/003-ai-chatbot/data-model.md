# Data Model: Phase III – AI-Powered Todo Chatbot

**Feature**: Phase III – AI-Powered Todo Chatbot
**Date**: 2026-02-07
**Author**: Claude Code

## Overview

This document defines the data model for the AI-powered todo chatbot application, specifying entities, relationships, and validation rules that will be implemented using SQLModel with Neon PostgreSQL.

## Entity Definitions

### User
Represents an authenticated user of the system.

**Fields:**
- `id` (UUID, Primary Key) - Unique identifier for the user
- `email` (String, 255, Unique, Required) - User's email address
- `first_name` (String, 100, Optional) - User's first name
- `last_name` (String, 100, Optional) - User's last name
- `created_at` (DateTime, Required) - Timestamp when user was created
- `updated_at` (DateTime, Required) - Timestamp when user was last updated
- `is_active` (Boolean, Required, Default: True) - Whether the account is active

**Validation:**
- Email must be valid email format
- Email must be unique across all users

### Todo
Represents a task item owned by a user.

**Fields:**
- `id` (Integer, Primary Key, Auto-increment) - Unique identifier for the todo
- `title` (String, 200, Required) - Title of the task
- `description` (String, 1000, Optional) - Detailed description of the task
- `status` (Enum: 'pending', 'completed', Required, Default: 'pending') - Current status of the task
- `priority` (Enum: 'low', 'medium', 'high', Required, Default: 'medium') - Priority level of the task
- `due_date` (DateTime, Optional) - Due date for the task
- `user_id` (UUID, Foreign Key, Required) - Reference to the owning user
- `created_at` (DateTime, Required) - Timestamp when todo was created
- `updated_at` (DateTime, Required) - Timestamp when todo was last updated

**Validation:**
- Title must be 1-200 characters
- Description, if provided, must be 1-1000 characters
- Status must be one of 'pending' or 'completed'
- Priority must be one of 'low', 'medium', 'high'

**Relationships:**
- Belongs to one User (many-to-one with User)

### Conversation
Represents a chat session between a user and the AI assistant.

**Fields:**
- `id` (UUID, Primary Key) - Unique identifier for the conversation
- `title` (String, 200, Optional) - Title for the conversation (auto-generated from first message if not provided)
- `user_id` (UUID, Foreign Key, Required) - Reference to the user who owns the conversation
- `created_at` (DateTime, Required) - Timestamp when conversation was started
- `updated_at` (DateTime, Required) - Timestamp when conversation was last updated

**Validation:**
- Title, if provided, must be 1-200 characters

**Relationships:**
- Belongs to one User (many-to-one with User)
- Has many Messages (one-to-many with Message)

### Message
Represents an individual message within a conversation.

**Fields:**
- `id` (UUID, Primary Key) - Unique identifier for the message
- `conversation_id` (UUID, Foreign Key, Required) - Reference to the parent conversation
- `role` (Enum: 'user', 'assistant', Required) - The sender of the message ('user' for user, 'assistant' for AI)
- `content` (Text, Required) - The content of the message
- `timestamp` (DateTime, Required) - When the message was sent
- `metadata` (JSON, Optional) - Additional data about the message (tool calls, etc.)

**Validation:**
- Content must be 1-10000 characters
- Role must be either 'user' or 'assistant'

**Relationships:**
- Belongs to one Conversation (many-to-one with Conversation)

## Relationships Summary

```
User (1) <---> (Many) Todo
User (1) <---> (Many) Conversation
Conversation (1) <---> (Many) Message
```

## Indexes

### Todo Table
- Index on `user_id` for efficient user-specific queries
- Index on `user_id` and `status` for filtered queries
- Index on `user_id` and `priority` for priority-based sorting
- Index on `user_id` and `due_date` for deadline-based queries

### Conversation Table
- Index on `user_id` for efficient user-specific queries
- Index on `created_at` for chronological ordering

### Message Table
- Index on `conversation_id` for conversation-specific queries
- Index on `timestamp` for chronological ordering
- Composite index on `conversation_id` and `timestamp` for efficient conversation history retrieval

## Constraints

1. **Referential Integrity**: Foreign key constraints ensure data consistency between related tables
2. **Data Isolation**: All queries must filter by `user_id` to prevent cross-user data access
3. **Required Fields**: All required fields must be present during creation
4. **Value Validation**: Enum fields must contain valid values only

## State Transitions

### Todo Status Transitions
- `pending` → `completed` (when user marks task as complete)
- `completed` → `pending` (when user marks task as incomplete)

## Business Rules

1. **User Ownership**: All todos and conversations belong to exactly one user
2. **Access Control**: Users can only access their own data
3. **Data Persistence**: Conversation history is persisted for continuity across sessions
4. **Message Ordering**: Messages within conversations are ordered chronologically by timestamp