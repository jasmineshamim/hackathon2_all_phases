# Todo API Contract

## Overview
This document defines the API contracts for the todo application with AI chatbot functionality. All endpoints require JWT authentication in the Authorization header.

## Base URL
`http://localhost:8000/api/v1` (development)

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

## Endpoints

### Todo Management

#### GET /todos
Retrieve all todos for the authenticated user.

**Headers:**
- Authorization: Bearer <jwt_token>

**Query Parameters:**
- status (optional): Filter by status (pending|completed)
- priority (optional): Filter by priority (low|medium|high)
- limit (optional): Number of results to return (default: 50)
- offset (optional): Offset for pagination (default: 0)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "todos": [
      {
        "id": 1,
        "title": "Sample task",
        "description": "Task description",
        "status": "pending",
        "priority": "medium",
        "due_date": "2023-12-31T10:00:00Z",
        "created_at": "2023-12-01T10:00:00Z",
        "updated_at": "2023-12-01T10:00:00Z"
      }
    ],
    "total": 1
  },
  "message": "Todos retrieved successfully"
}
```

#### POST /todos
Create a new todo.

**Headers:**
- Authorization: Bearer <jwt_token>
- Content-Type: application/json

**Request Body:**
```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "priority": "medium (optional, default: medium)",
  "due_date": "2023-12-31T10:00:00Z (optional)"
}
```

**Validation:**
- title: required, 1-200 characters
- description: optional, 0-1000 characters
- priority: optional, enum (low, medium, high)
- due_date: optional, ISO 8601 datetime

**Response (201):**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "status": "pending",
      "priority": "medium",
      "due_date": "2023-12-31T10:00:00Z",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  },
  "message": "Todo created successfully"
}
```

#### PUT /todos/{todo_id}
Update an existing todo.

**Headers:**
- Authorization: Bearer <jwt_token>
- Content-Type: application/json

**Path Parameters:**
- todo_id: Integer ID of the todo to update

**Request Body:**
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)",
  "status": "completed (optional, enum: pending, completed)",
  "priority": "high (optional, enum: low, medium, high)",
  "due_date": "2023-12-31T10:00:00Z (optional)"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": 1,
      "title": "Updated title",
      "description": "Updated description",
      "status": "completed",
      "priority": "high",
      "due_date": "2023-12-31T10:00:00Z",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-02T10:00:00Z"
    }
  },
  "message": "Todo updated successfully"
}
```

#### DELETE /todos/{todo_id}
Delete a todo.

**Headers:**
- Authorization: Bearer <jwt_token>

**Path Parameters:**
- todo_id: Integer ID of the todo to delete

**Response (200):**
```json
{
  "success": true,
  "data": {
    "deleted_id": 1
  },
  "message": "Todo deleted successfully"
}
```

#### PUT /todos/{todo_id}/toggle-status
Toggle the status of a todo between pending and completed.

**Headers:**
- Authorization: Bearer <jwt_token>

**Path Parameters:**
- todo_id: Integer ID of the todo to update

**Response (200):**
```json
{
  "success": true,
  "data": {
    "todo": {
      "id": 1,
      "title": "Task title",
      "status": "completed"
    }
  },
  "message": "Todo status updated successfully"
}
```

### Chat and Conversation Management

#### POST /chat
Send a message to the AI chatbot and receive a response.

**Headers:**
- Authorization: Bearer <jwt_token>
- Content-Type: application/json

**Request Body:**
```json
{
  "message": "User's message to the chatbot (required)",
  "conversation_id": "UUID of existing conversation (optional, creates new if not provided)"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "response": "AI's response to the user",
    "conversation_id": "UUID of the conversation",
    "next_action": {
      "type": "show_todos|create_todo|update_todo|delete_todo|etc",
      "payload": {}
    }
  },
  "message": "Message processed successfully"
}
```

#### GET /conversations
Get a list of conversations for the authenticated user.

**Headers:**
- Authorization: Bearer <jwt_token>

**Query Parameters:**
- limit (optional): Number of results to return (default: 20)
- offset (optional): Offset for pagination (default: 0)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": "uuid-of-conversation",
        "title": "Conversation title",
        "created_at": "2023-12-01T10:00:00Z",
        "updated_at": "2023-12-01T10:00:00Z"
      }
    ],
    "total": 1
  },
  "message": "Conversations retrieved successfully"
}
```

#### GET /conversations/{conversation_id}/messages
Get messages for a specific conversation.

**Headers:**
- Authorization: Bearer <jwt_token>

**Path Parameters:**
- conversation_id: UUID of the conversation

**Query Parameters:**
- limit (optional): Number of results to return (default: 50)
- offset (optional): Offset for pagination (default: 0)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": "uuid-of-message",
        "role": "user",
        "content": "User message content",
        "timestamp": "2023-12-01T10:00:00Z"
      },
      {
        "id": "uuid-of-message",
        "role": "assistant",
        "content": "Assistant response content",
        "timestamp": "2023-12-01T10:00:05Z"
      }
    ]
  },
  "message": "Messages retrieved successfully"
}
```

### Health Check

#### GET /health
Health check endpoint for monitoring.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-01T10:00:00Z",
  "version": "1.0.0"
}
```

## Error Codes

- `AUTH_001`: Unauthorized - Invalid or missing JWT token
- `AUTH_002`: Forbidden - User doesn't have permission for this resource
- `VALIDATION_ERROR`: Request validation failed
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INTERNAL_ERROR`: Internal server error occurred
- `RATE_LIMIT_EXCEEDED`: Too many requests from this user