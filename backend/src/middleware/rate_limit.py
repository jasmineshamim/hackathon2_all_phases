"""Rate limiting middleware."""
from fastapi import Request, HTTPException, status
from typing import Dict
from datetime import datetime, timedelta
import asyncio


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        self.cleanup_interval = 60  # seconds

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request."""
        # Try to get user from auth, otherwise use IP
        user_id = getattr(request.state, 'user_id', None)
        if user_id:
            return f"user:{user_id}"

        # Fallback to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0]}"

        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def _cleanup_old_requests(self, client_id: str):
        """Remove requests older than 1 minute."""
        if client_id not in self.requests:
            return

        cutoff_time = datetime.utcnow() - timedelta(minutes=1)
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff_time
        ]

    async def check_rate_limit(self, request: Request):
        """Check if request should be rate limited."""
        client_id = self._get_client_id(request)

        # Cleanup old requests
        self._cleanup_old_requests(client_id)

        # Initialize if new client
        if client_id not in self.requests:
            self.requests[client_id] = []

        # Check rate limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please try again later.",
                        "retry_after": 60
                    }
                }
            )

        # Add current request
        self.requests[client_id].append(datetime.utcnow())


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    # Skip rate limiting for health checks
    if request.url.path.startswith("/health"):
        return await call_next(request)

    # Check rate limit
    await rate_limiter.check_rate_limit(request)

    # Process request
    response = await call_next(request)
    return response
