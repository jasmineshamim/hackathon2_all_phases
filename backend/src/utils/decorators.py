"""Authentication decorators for API endpoints."""
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from backend.src.middleware.auth import security, get_current_user_id
from typing import Callable
import uuid


def require_auth(func: Callable):
    """Decorator to require authentication for an endpoint."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract credentials from kwargs
        credentials = kwargs.get('credentials')
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify and extract user_id
        user_id = await get_current_user_id(credentials)
        kwargs['user_id'] = uuid.UUID(user_id)

        return await func(*args, **kwargs)

    return wrapper


def get_authenticated_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> uuid.UUID:
    """Dependency to get authenticated user ID."""
    import asyncio
    user_id_str = asyncio.run(get_current_user_id(credentials))
    return uuid.UUID(user_id_str)
