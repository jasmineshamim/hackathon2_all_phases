# API Contracts: Todo Full-Stack Web Application

## Task Management API

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the specified user
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID to retrieve tasks for
**Response**: 200 OK with array of Task objects
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path

### POST /api/{user_id}/tasks
**Description**: Create a new task for the specified user
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID to create task for
**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, 1-1000 chars)"
}
```
**Response**: 201 Created with created Task object
**Error Responses**:
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for the specified user
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID
- `id` (path): Task ID
**Response**: 200 OK with Task object
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path
- 404 Not Found: Task does not exist

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for the specified user
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID
- `id` (path): Task ID
**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, 1-1000 chars)"
}
```
**Response**: 200 OK with updated Task object
**Error Responses**:
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path
- 404 Not Found: Task does not exist

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for the specified user
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID
- `id` (path): Task ID
**Response**: 204 No Content
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path
- 404 Not Found: Task does not exist

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle completion status of a specific task
**Authentication**: JWT token required
**Authorization**: User must match the user_id in the path
**Parameters**:
- `user_id` (path): User ID
- `id` (path): Task ID
**Request Body**:
```json
{
  "completed": "boolean"
}
```
**Response**: 200 OK with updated Task object
**Error Responses**:
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User does not match user_id in path
- 404 Not Found: Task does not exist

## Task Object Schema

```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "datetime string",
  "updated_at": "datetime string"
}
```

## Authentication API (Better Auth)

### POST /api/auth/register
**Description**: Register a new user
**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string (optional)"
}
```
**Response**: 200 OK with JWT token
**Error Responses**:
- 400 Bad Request: Invalid registration data
- 409 Conflict: User already exists

### POST /api/auth/login
**Description**: Login existing user
**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```
**Response**: 200 OK with JWT token
**Error Responses**:
- 400 Bad Request: Invalid login data
- 401 Unauthorized: Invalid credentials