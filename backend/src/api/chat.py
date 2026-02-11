"""Chat API endpoints for natural language todo management."""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session
from pydantic import BaseModel
import uuid

from database.models.base import get_session
from database.models.message import MessageRole
from backend.src.services.ai_agent_service import AIAgentService
from backend.src.services.todo_service import TodoService
from backend.src.services.conversation_service import ConversationService
from backend.src.middleware.auth import security, get_current_user_id
from backend.src.utils.errors import format_error_response, APIError

router = APIRouter()


# Request/Response Models
class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: str
    next_action: Optional[Dict[str, Any]] = None


@router.post("/", response_model=dict)
async def process_chat_message(
    chat_data: ChatMessage,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Process a chat message and return AI response."""
    try:
        user_id = await get_current_user_id(credentials)
        user_uuid = uuid.UUID(user_id)

        # Initialize services
        ai_service = AIAgentService()
        todo_service = TodoService(session)
        conversation_service = ConversationService(session)

        # Get or create conversation
        conversation_uuid = None
        conversation_history = None

        if chat_data.conversation_id:
            conversation_uuid = uuid.UUID(chat_data.conversation_id)
            # Load conversation history
            conversation_history = conversation_service.get_conversation_history(
                user_id=user_uuid,
                conversation_id=conversation_uuid
            )
        else:
            # Create new conversation
            conversation = conversation_service.create_conversation(
                user_id=user_uuid,
                title=f"Chat {chat_data.message[:30]}..."
            )
            conversation_uuid = conversation.id

        # Store user message
        conversation_service.add_message(
            user_id=user_uuid,
            conversation_id=conversation_uuid,
            role=MessageRole.USER,
            content=chat_data.message
        )

        # Define MCP tool executor
        async def execute_mcp_tool(function_name: str, arguments: dict) -> dict:
            """Execute MCP tool based on function name."""
            if function_name == "create_todo":
                todo = todo_service.create_todo(
                    user_id=user_uuid,
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    priority=arguments.get("priority", "medium"),
                    due_date=arguments.get("due_date")
                )
                return {
                    "success": True,
                    "todo": {
                        "id": todo.id,
                        "title": todo.title,
                        "status": todo.status.value
                    }
                }

            elif function_name == "list_todos":
                todos = todo_service.get_todos(
                    user_id=user_uuid,
                    status=arguments.get("status"),
                    priority=arguments.get("priority")
                )
                return {
                    "success": True,
                    "todos": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "status": t.status.value,
                            "priority": t.priority.value
                        }
                        for t in todos
                    ],
                    "total": len(todos)
                }

            elif function_name == "update_todo":
                todo = todo_service.update_todo(
                    user_id=user_uuid,
                    todo_id=arguments.get("todo_id"),
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    status=arguments.get("status"),
                    priority=arguments.get("priority")
                )
                return {
                    "success": True,
                    "todo": {
                        "id": todo.id,
                        "title": todo.title,
                        "status": todo.status.value
                    }
                }

            elif function_name == "delete_todo":
                deleted_id = todo_service.delete_todo(
                    user_id=user_uuid,
                    todo_id=arguments.get("todo_id")
                )
                return {
                    "success": True,
                    "deleted_id": deleted_id
                }

            elif function_name == "toggle_todo_status":
                todo = todo_service.toggle_todo_status(
                    user_id=user_uuid,
                    todo_id=arguments.get("todo_id")
                )
                return {
                    "success": True,
                    "todo": {
                        "id": todo.id,
                        "title": todo.title,
                        "status": todo.status.value
                    }
                }

            return {"success": False, "error": "Unknown function"}

        # Process the message
        ai_response = await ai_service.process_message(
            message=chat_data.message,
            conversation_history=conversation_history,
            mcp_tool_executor=execute_mcp_tool
        )

        # Format response
        formatted_response = ai_service.format_response_for_chat(ai_response)

        # Store assistant response
        conversation_service.add_message(
            user_id=user_uuid,
            conversation_id=conversation_uuid,
            role=MessageRole.ASSISTANT,
            content=formatted_response,
            metadata={
                "tool_calls": ai_response.get("tool_calls", [])
            }
        )

        return {
            "success": True,
            "data": {
                "response": formatted_response,
                "conversation_id": str(conversation_uuid),
                "next_action": None
            },
            "message": "Message processed successfully"
        }

    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.get("/conversations", response_model=dict)
async def get_conversations(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get all conversations for the authenticated user."""
    try:
        user_id = await get_current_user_id(credentials)
        user_uuid = uuid.UUID(user_id)

        conversation_service = ConversationService(session)
        conversations = conversation_service.get_conversations(
            user_id=user_uuid,
            limit=limit,
            offset=offset
        )

        return {
            "success": True,
            "data": {
                "conversations": [
                    {
                        "id": str(conv.id),
                        "title": conv.title,
                        "created_at": conv.created_at.isoformat(),
                        "updated_at": conv.updated_at.isoformat()
                    }
                    for conv in conversations
                ],
                "total": len(conversations)
            },
            "message": "Conversations retrieved successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))


@router.get("/conversations/{conversation_id}/messages", response_model=dict)
async def get_conversation_messages(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get messages for a specific conversation."""
    try:
        user_id = await get_current_user_id(credentials)
        user_uuid = uuid.UUID(user_id)
        conversation_uuid = uuid.UUID(conversation_id)

        conversation_service = ConversationService(session)
        messages = conversation_service.get_conversation_messages(
            user_id=user_uuid,
            conversation_id=conversation_uuid,
            limit=limit,
            offset=offset
        )

        return {
            "success": True,
            "data": {
                "messages": [
                    {
                        "id": str(msg.id),
                        "role": msg.role.value,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in messages
                ]
            },
            "message": "Messages retrieved successfully"
        }
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=format_error_response(e))

