"""
Pagination utilities for LinkDB API.

Provides consistent pagination across all endpoints.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field
from fastapi import Query

from config import settings


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(1, ge=1, description="Page number (starts at 1)")
    page_size: int = Field(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description=f"Items per page (max {settings.MAX_PAGE_SIZE})"
    )

    @property
    def offset(self) -> int:
        """Calculate offset from page number."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit (alias for page_size)."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response format.

    Provides consistent pagination metadata across all endpoints.
    """

    items: List[T] = Field(description="List of items for current page")
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "items": [{"id": 1, "name": "Example"}],
                "total": 100,
                "page": 1,
                "page_size": 50,
                "total_pages": 2,
                "has_next": True,
                "has_prev": False
            }
        }


def create_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description=f"Items per page (max {settings.MAX_PAGE_SIZE})"
    )
) -> PaginationParams:
    """
    Create pagination parameters from query params.

    Use as a FastAPI dependency:

        @app.get("/items")
        def get_items(pagination: PaginationParams = Depends(create_pagination_params)):
            offset = pagination.offset
            limit = pagination.limit
            # Use offset and limit in query
    """
    return PaginationParams(page=page, page_size=page_size)


def paginate(
    items: List[T],
    total: int,
    params: PaginationParams
) -> PaginatedResponse[T]:
    """
    Create a paginated response from items and total count.

    Args:
        items: List of items for current page
        total: Total number of items across all pages
        params: Pagination parameters

    Returns:
        PaginatedResponse with metadata

    Example:
        # Get pagination params from request
        params = PaginationParams(page=1, page_size=50)

        # Query database
        total = cursor.execute("SELECT COUNT(*) FROM table").fetchone()[0]
        items = cursor.execute(
            "SELECT * FROM table LIMIT ? OFFSET ?",
            (params.limit, params.offset)
        ).fetchall()

        # Create paginated response
        response = paginate(items, total, params)
    """
    total_pages = (total + params.page_size - 1) // params.page_size if total > 0 else 0

    return PaginatedResponse(
        items=items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        has_next=params.page < total_pages,
        has_prev=params.page > 1
    )


def paginate_query(
    cursor,
    query: str,
    count_query: str,
    params: tuple,
    pagination: PaginationParams
) -> tuple[List, int]:
    """
    Execute a paginated query and return results with total count.

    Args:
        cursor: Database cursor
        query: SELECT query (without LIMIT/OFFSET)
        count_query: COUNT query to get total
        params: Query parameters
        pagination: Pagination parameters

    Returns:
        Tuple of (items, total)

    Example:
        cursor = conn.cursor()
        items, total = paginate_query(
            cursor,
            query="SELECT * FROM customer_history WHERE customer_id = ?",
            count_query="SELECT COUNT(*) FROM customer_history WHERE customer_id = ?",
            params=(customer_id,),
            pagination=pagination_params
        )
    """
    # Get total count
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    # Get paginated items
    paginated_query = f"{query} LIMIT ? OFFSET ?"
    cursor.execute(paginated_query, params + (pagination.limit, pagination.offset))
    items = cursor.fetchall()

    return items, total


# Export main functions and classes
__all__ = [
    'PaginationParams',
    'PaginatedResponse',
    'create_pagination_params',
    'paginate',
    'paginate_query'
]
