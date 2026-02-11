"""Health check endpoint."""
from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "Todo Chatbot API",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@router.get("/health/db")
async def database_health():
    """Database health check."""
    try:
        from database.models.base import engine
        from sqlmodel import text, Session

        with Session(engine) as session:
            session.exec(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
