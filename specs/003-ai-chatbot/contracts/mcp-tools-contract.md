# MCP Tools Contract

## Overview
This document defines the Model Context Protocol (MCP) tools that the AI agent can discover and invoke to perform todo operations. These tools provide a standardized interface between the AI agent and the backend service.

## Tool Discovery
The MCP server supports tool discovery at the `/tools` endpoint, returning a list of available tools in the MCP format.

## Tools

### 1. create-todo
Creates a new todo item.

**Tool Name**: `create-todo`

**Description**: Creates a new todo item with the specified title and optional details.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Title of the task (required)"
    },
    "description": {
      "type": "string",
      "description": "Detailed description of the task (optional)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Priority level of the task (optional, default: medium)"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "Due date for the task in ISO 8601 format (optional)"
    }
  },
  "required": ["title"]
}
```

**Authentication**: Requires JWT token in MCP context

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "data": {
      "type": "object",
      "properties": {
        "todo": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "title": {
              "type": "string"
            },
            "description": {
              "type": "string"
            },
            "status": {
              "type": "string",
              "enum": ["pending", "completed"]
            },
            "priority": {
              "type": "string",
              "enum": ["low", "medium", "high"]
            },
            "due_date": {
              "type": "string",
              "format": "date-time"
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "updated_at": {
              "type": "string",
              "format": "date-time"
            }
          }
        }
      }
    },
    "message": {
      "type": "string"
    }
  }
}
```

### 2. list-todos
Retrieves all todos for the authenticated user.

**Tool Name**: `list-todos`

**Description**: Retrieves all todo items for the authenticated user, with optional filtering.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["pending", "completed"],
      "description": "Filter by status (optional)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "Filter by priority (optional)"
    }
  }
}
```

**Authentication**: Requires JWT token in MCP context

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "data": {
      "type": "object",
      "properties": {
        "todos": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "title": {
                "type": "string"
              },
              "description": {
                "type": "string"
              },
              "status": {
                "type": "string",
                "enum": ["pending", "completed"]
              },
              "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"]
              },
              "due_date": {
                "type": "string",
                "format": "date-time"
              },
              "created_at": {
                "type": "string",
                "format": "date-time"
              },
              "updated_at": {
                "type": "string",
                "format": "date-time"
              }
            }
          }
        },
        "total": {
          "type": "integer"
        }
      }
    },
    "message": {
      "type": "string"
    }
  }
}
```

### 3. update-todo
Updates an existing todo item.

**Tool Name**: `update-todo`

**Description**: Updates an existing todo item with the specified changes.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "todo_id": {
      "type": "integer",
      "description": "ID of the todo to update (required)"
    },
    "title": {
      "type": "string",
      "description": "New title for the task (optional)"
    },
    "description": {
      "type": "string",
      "description": "New description for the task (optional)"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "completed"],
      "description": "New status for the task (optional)"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "description": "New priority for the task (optional)"
    },
    "due_date": {
      "type": "string",
      "format": "date-time",
      "description": "New due date for the task (optional)"
    }
  },
  "required": ["todo_id"]
}
```

**Authentication**: Requires JWT token in MCP context

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "data": {
      "type": "object",
      "properties": {
        "todo": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "title": {
              "type": "string"
            },
            "description": {
              "type": "string"
            },
            "status": {
              "type": "string",
              "enum": ["pending", "completed"]
            },
            "priority": {
              "type": "string",
              "enum": ["low", "medium", "high"]
            },
            "due_date": {
              "type": "string",
              "format": "date-time"
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "updated_at": {
              "type": "string",
              "format": "date-time"
            }
          }
        }
      }
    },
    "message": {
      "type": "string"
    }
  }
}
```

### 4. delete-todo
Deletes a todo item.

**Tool Name**: `delete-todo`

**Description**: Deletes a todo item by ID.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "todo_id": {
      "type": "integer",
      "description": "ID of the todo to delete (required)"
    }
  },
  "required": ["todo_id"]
}
```

**Authentication**: Requires JWT token in MCP context

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "data": {
      "type": "object",
      "properties": {
        "deleted_id": {
          "type": "integer"
        }
      }
    },
    "message": {
      "type": "string"
    }
  }
}
```

### 5. toggle-todo-status
Toggles the status of a todo between pending and completed.

**Tool Name**: `toggle-todo-status`

**Description**: Toggles the status of a todo item between pending and completed.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "todo_id": {
      "type": "integer",
      "description": "ID of the todo to toggle (required)"
    }
  },
  "required": ["todo_id"]
}
```

**Authentication**: Requires JWT token in MCP context

**Response Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean"
    },
    "data": {
      "type": "object",
      "properties": {
        "todo": {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "title": {
              "type": "string"
            },
            "status": {
              "type": "string",
              "enum": ["pending", "completed"]
            }
          }
        }
      }
    },
    "message": {
      "type": "string"
    }
  }
}
```

## Authentication and Authorization

### JWT Token Context
All MCP tools receive the user's JWT token as part of the context and must validate it before performing operations. Each tool operates within the security context of the authenticated user and can only access that user's data.

### User Isolation
- All queries must filter by the authenticated user's ID
- Users cannot access or modify other users' data
- MCP tools must enforce user isolation at the database level

## Error Handling

### Standard Error Response
All tools return errors in the following format:
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

### Common Error Codes
- `INVALID_INPUT`: Provided parameters failed validation
- `UNAUTHORIZED`: JWT token is invalid or expired
- `FORBIDDEN`: User doesn't have permission to access the resource
- `RESOURCE_NOT_FOUND`: Requested todo item doesn't exist
- `INTERNAL_ERROR`: Unexpected server error occurred