"""
Request tracking middleware.

Assigns unique ID to each request and tracks performance metrics.
"""

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from logging_config import log_request, log_response, log_error


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track all HTTP requests.

    Features:
    - Assigns unique request ID
    - Logs request start and completion
    - Tracks request duration
    - Adds request ID to response headers
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Process request and track metrics."""
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Store request ID in request state for access in route handlers
        request.state.request_id = request_id

        # Log request start
        log_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else "unknown"
        )

        # Record start time
        start_time = time.time()

        try:
            # Process request
            response: Response = await call_next(request)

            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Log response
            log_response(
                request_id=request_id,
                status_code=response.status_code,
                duration_ms=duration_ms
            )

            # Add request ID to response headers for client-side tracking
            response.headers["X-Request-ID"] = request_id

            # Add performance timing header
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

            return response

        except Exception as e:
            # Calculate duration even on error
            duration_ms = (time.time() - start_time) * 1000

            # Log error
            log_error(
                request_id=request_id,
                error=e,
                context={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms
                }
            )

            # Re-raise the exception to be handled by FastAPI's exception handlers
            raise
