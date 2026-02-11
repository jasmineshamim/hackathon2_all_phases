"""
Chat endpoint for AI-powered task management conversations.
Handles POST /api/{user_id}/chat requests.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from models.message import MessageRole
from src.agents.chat_agent import chat_agent
from src.agents.prompts import SYSTEM_PROMPT
from database import get_session
from sqlmodel import Session

router = APIRouter()

# Request/Response Models

class ChatRequest(BaseModel):
    """Chat request payload."""
    conversation_id: Optional[int] = Field(None, description="Optional conversation ID to continue")
    message: str = Field(..., description="User's message", min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    """Chat response payload."""
    conversation_id: int = Field(description="Conversation ID (new or existing)")
    response: str = Field(description="AI assistant's response")
    tool_calls: List[Dict[str, Any]] = Field(default=[], description="Tools invoked during processing")

# Helper function to verify JWT token
def verify_jwt_token(authorization: str = Header(...)) -> str:
    """
    Verify JWT token and extract user_id.

    Args:
        authorization: Authorization header with Bearer token

    Returns:
        user_id from token

    Raises:
        HTTPException: If token is invalid
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.replace("Bearer ", "")

    # Import JWT handler functions
    try:
        from auth.jwt_handler import get_user_id_from_token
    except ImportError:
        from backend.auth.jwt_handler import get_user_id_from_token

    # Verify token and extract user ID
    try:
        user_id = get_user_id_from_token(token)
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    token_user_id: str = Depends(verify_jwt_token)
):
    """
    Send message to AI chatbot and receive response.

    Args:
        user_id: User ID from path (must match token)
        request: Chat request with message and optional conversation_id
        session: Database session
        token_user_id: User ID from JWT token

    Returns:
        ChatResponse with conversation_id, response, and tool_calls

    Raises:
        HTTPException: If validation fails or error occurs
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match authenticated user"
        )

    # Validate message length
    if len(request.message) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Message must be max 2000 characters"
        )

    try:
        # Initialize services
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Get or create conversation
        conversation = await conversation_service.get_or_create_conversation(
            user_id=user_id,
            conversation_id=request.conversation_id
        )

        # Store user message
        await message_service.store_message(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.USER,
            content=request.message
        )

        # Build message array for agent
        messages = await message_service.build_message_array(
            conversation_id=conversation.id,
            new_message=request.message,
            system_prompt=SYSTEM_PROMPT
        )

        # Process message with agent
        agent_response = await chat_agent.process_message(
            messages=messages,
            user_id=user_id
        )

        # Store assistant response
        await message_service.store_message(
            conversation_id=conversation.id,
            user_id=user_id,
            role=MessageRole.ASSISTANT,
            content=agent_response["response"]
        )

        # Update conversation timestamp
        await conversation_service.update_conversation_timestamp(conversation.id)

        # Return response
        return ChatResponse(
            conversation_id=conversation.id,
            response=agent_response["response"],
            tool_calls=agent_response.get("tool_calls", [])
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred processing your request: {str(e)}"
        )
