"""API error handling utilities."""
from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class APIError(Exception):
    """Base API error class."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(APIError):
    """Authentication error."""

    def __init__(self, message: str = "Invalid or missing authentication token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTH_001",
            message=message
        )


class AuthorizationError(APIError):
    """Authorization error."""

    def __init__(self, message: str = "User doesn't have permission for this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTH_002",
            message=message
        )


class ValidationError(APIError):
    """Validation error."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class ResourceNotFoundError(APIError):
    """Resource not found error."""

    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
            message=f"{resource} with id {resource_id} not found"
        )


class InternalServerError(APIError):
    """Internal server error."""

    def __init__(self, message: str = "An internal server error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message=message
        )


class RateLimitError(APIError):
    """Rate limit exceeded error."""

    def __init__(self, message: str = "Too many requests from this user"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            message=message
        )


def format_error_response(error: APIError) -> dict:
    """Format error response for API."""
    return {
        "success": False,
        "error": {
            "code": error.error_code,
            "message": error.message,
            "details": error.details
        }
    }
