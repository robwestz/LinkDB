"""
Input validation and sanitization for LinkDB API.

Prevents SQL injection, validates data formats, and ensures data integrity.
"""

from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from datetime import datetime
import re


class CustomerQuery(BaseModel):
    """Validation for customer query parameters."""

    customer_id: int = Field(..., gt=0, description="Customer ID must be positive")

    @validator('customer_id')
    def validate_customer_id(cls, v):
        """Ensure customer ID is within reasonable range."""
        if v > 1000000:  # Arbitrary large number
            raise ValueError('customer_id is unreasonably large')
        return v


class DateRangeQuery(BaseModel):
    """Validation for date range queries."""

    from_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$', description="Format: YYYY-MM")
    to_date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}$', description="Format: YYYY-MM")

    @validator('from_date', 'to_date')
    def validate_date_format(cls, v):
        """Validate date is in YYYY-MM format and is a valid date."""
        if v is None:
            return v

        try:
            year, month = map(int, v.split('-'))
            if year < 1900 or year > 2100:
                raise ValueError('Year must be between 1900 and 2100')
            if month < 1 or month > 12:
                raise ValueError('Month must be between 1 and 12')
            return v
        except ValueError as e:
            raise ValueError(f'Invalid date format: {e}')

    @validator('to_date')
    def validate_date_range(cls, v, values):
        """Ensure from_date is before or equal to to_date."""
        if v and 'from_date' in values and values['from_date']:
            if values['from_date'] > v:
                raise ValueError('from_date must be before or equal to to_date')
        return v


class PaginationQuery(BaseModel):
    """Validation for pagination parameters."""

    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(50, ge=1, le=100, description="Number of items to return (max 100)")

    @validator('offset')
    def validate_offset(cls, v):
        """Ensure offset is reasonable."""
        if v > 1000000:  # Prevent unreasonable offsets
            raise ValueError('offset is too large')
        return v


class SearchQuery(BaseModel):
    """Validation for search parameters."""

    search_term: str = Field(..., min_length=1, max_length=200)
    case_sensitive: bool = Field(False)

    @validator('search_term')
    def sanitize_search_term(cls, v):
        """Sanitize search term to prevent SQL injection."""
        # Remove any SQL keywords and special characters that could be dangerous
        dangerous_patterns = [
            r';',  # SQL statement terminator
            r'--',  # SQL comment
            r'/\*',  # SQL comment start
            r'\*/',  # SQL comment end
            r'xp_',  # Extended stored procedures
            r'sp_',  # System stored procedures
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(f'Search term contains invalid pattern: {pattern}')

        return v.strip()


class LinkCreateValidation(BaseModel):
    """Validation for creating new links."""

    customer_id: int = Field(..., gt=0)
    canonical_root: str = Field(..., min_length=3, max_length=255)
    brand: str = Field(..., min_length=1, max_length=255)
    pub_domain: str = Field(..., min_length=3, max_length=255)
    target_url: str = Field(..., min_length=5, max_length=2048)
    anchor_text: str = Field(..., min_length=1, max_length=500)
    published_at: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')

    @validator('pub_domain', 'canonical_root')
    def validate_domain(cls, v):
        """Validate domain format."""
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        if not re.match(domain_pattern, v):
            raise ValueError(f'Invalid domain format: {v}')
        return v.lower()

    @validator('target_url')
    def validate_url(cls, v):
        """Validate URL format."""
        url_pattern = r'^https?:\/\/'
        if not re.match(url_pattern, v, re.IGNORECASE):
            # Automatically prepend http:// if missing
            v = f'http://{v}'
        return v

    @validator('published_at')
    def validate_published_date(cls, v):
        """Validate date is in YYYY-MM-DD format and is reasonable."""
        try:
            date = datetime.strptime(v, '%Y-%m-%d')

            # Check if date is not in the future
            if date > datetime.now():
                raise ValueError('published_at cannot be in the future')

            # Check if date is not too old (before year 2000)
            if date.year < 2000:
                raise ValueError('published_at cannot be before year 2000')

            return v
        except ValueError as e:
            raise ValueError(f'Invalid date: {e}')


class LinkUpdateValidation(BaseModel):
    """Validation for updating existing links."""

    pub_domain: Optional[str] = Field(None, min_length=3, max_length=255)
    target_url: Optional[str] = Field(None, min_length=5, max_length=2048)
    anchor_text: Optional[str] = Field(None, min_length=1, max_length=500)
    published_at: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')

    @validator('pub_domain')
    def validate_domain(cls, v):
        """Validate domain format if provided."""
        if v is None:
            return v

        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        if not re.match(domain_pattern, v):
            raise ValueError(f'Invalid domain format: {v}')
        return v.lower()

    @validator('target_url')
    def validate_url(cls, v):
        """Validate URL format if provided."""
        if v is None:
            return v

        url_pattern = r'^https?:\/\/'
        if not re.match(url_pattern, v, re.IGNORECASE):
            v = f'http://{v}'
        return v

    @validator('published_at')
    def validate_published_date(cls, v):
        """Validate date if provided."""
        if v is None:
            return v

        try:
            date = datetime.strptime(v, '%Y-%m-%d')

            if date > datetime.now():
                raise ValueError('published_at cannot be in the future')

            if date.year < 2000:
                raise ValueError('published_at cannot be before year 2000')

            return v
        except ValueError as e:
            raise ValueError(f'Invalid date: {e}')


class ComparisonQuery(BaseModel):
    """Validation for period comparison queries."""

    period1_from: str = Field(..., pattern=r'^\d{4}-\d{2}$')
    period1_to: str = Field(..., pattern=r'^\d{4}-\d{2}$')
    period2_from: str = Field(..., pattern=r'^\d{4}-\d{2}$')
    period2_to: str = Field(..., pattern=r'^\d{4}-\d{2}$')

    @validator('period1_from', 'period1_to', 'period2_from', 'period2_to')
    def validate_date_format(cls, v):
        """Validate date format."""
        try:
            year, month = map(int, v.split('-'))
            if year < 1900 or year > 2100:
                raise ValueError('Year must be between 1900 and 2100')
            if month < 1 or month > 12:
                raise ValueError('Month must be between 1 and 12')
            return v
        except ValueError as e:
            raise ValueError(f'Invalid date format: {e}')

    @validator('period1_to')
    def validate_period1_range(cls, v, values):
        """Ensure period1 from is before to."""
        if 'period1_from' in values and values['period1_from'] > v:
            raise ValueError('period1_from must be before or equal to period1_to')
        return v

    @validator('period2_to')
    def validate_period2_range(cls, v, values):
        """Ensure period2 from is before to."""
        if 'period2_from' in values and values['period2_from'] > v:
            raise ValueError('period2_from must be before or equal to period2_to')
        return v


def sanitize_sql_parameter(param: any) -> any:
    """
    Sanitize a parameter before using in SQL query.

    This is a defense-in-depth measure. Always use parameterized queries as the primary defense.
    """
    if isinstance(param, str):
        # Remove any SQL keywords and dangerous characters
        dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in dangerous_chars:
            param = param.replace(char, '')
    return param


# Export validators
__all__ = [
    'CustomerQuery',
    'DateRangeQuery',
    'PaginationQuery',
    'SearchQuery',
    'LinkCreateValidation',
    'LinkUpdateValidation',
    'ComparisonQuery',
    'sanitize_sql_parameter'
]
