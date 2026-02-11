"""JWT authentication middleware."""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.src.utils.auth import decode_access_token, extract_user_id_from_token

security = HTTPBearer()


async def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials
) -> dict:
    """Verify JWT token from Authorization header."""
    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials
) -> str:
    """Extract current user ID from JWT token."""
    payload = await verify_jwt_token(credentials)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


class AuthMiddleware:
    """Authentication middleware for FastAPI."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        """Process request and verify authentication."""
        # Skip authentication for public endpoints
        public_paths = ["/", "/docs", "/redoc", "/openapi.json", "/health"]

        if request.url.path in public_paths:
            return await call_next(request)

        # Verify JWT token for protected endpoints
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add user info to request state
        request.state.user_id = payload.get("sub")
        request.state.user_email = payload.get("email")

        response = await call_next(request)
        return response
