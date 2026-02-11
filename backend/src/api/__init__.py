"""Base API router structure."""
from fastapi import APIRouter

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Import and include sub-routers here as they are created
# Example:
# from backend.src.api import todos, chat, mcp_tools
# api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
# api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
# api_router.include_router(mcp_tools.router, prefix="/mcp", tags=["mcp-tools"])
