"""
Unit tests for pagination utilities.

Tests:
- PaginationParams validation
- Offset calculation
- PaginatedResponse construction
- Paginate function
- Edge cases (empty results, single page, multiple pages)
"""

import pytest
from pydantic import ValidationError
from pagination import (
    PaginationParams,
    PaginatedResponse,
    paginate,
    create_pagination_params
)


@pytest.mark.unit
class TestPaginationParams:
    """Test PaginationParams model."""

    def test_default_values(self):
        """Test default pagination parameters."""
        params = PaginationParams()

        assert params.page == 1
        assert params.page_size == 50

    def test_custom_values(self):
        """Test custom pagination parameters."""
        params = PaginationParams(page=3, page_size=25)

        assert params.page == 3
        assert params.page_size == 25

    def test_offset_calculation(self):
        """Test offset property calculation."""
        # Page 1
        params = PaginationParams(page=1, page_size=50)
        assert params.offset == 0

        # Page 2
        params = PaginationParams(page=2, page_size=50)
        assert params.offset == 50

        # Page 3
        params = PaginationParams(page=3, page_size=25)
        assert params.offset == 50

        # Page 10
        params = PaginationParams(page=10, page_size=10)
        assert params.offset == 90

    def test_negative_page_rejected(self):
        """Test that negative page numbers are rejected."""
        with pytest.raises(ValidationError):
            PaginationParams(page=-1)

    def test_zero_page_rejected(self):
        """Test that page 0 is rejected."""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

    def test_zero_page_size_rejected(self):
        """Test that page_size 0 is rejected."""
        with pytest.raises(ValidationError):
            PaginationParams(page_size=0)

    def test_negative_page_size_rejected(self):
        """Test that negative page_size is rejected."""
        with pytest.raises(ValidationError):
            PaginationParams(page_size=-10)

    def test_page_size_exceeds_maximum(self):
        """Test that page_size > 100 is rejected."""
        with pytest.raises(ValidationError):
            PaginationParams(page_size=101)

    def test_page_size_at_maximum(self):
        """Test that page_size = 100 is allowed."""
        params = PaginationParams(page_size=100)
        assert params.page_size == 100


@pytest.mark.unit
class TestPaginatedResponse:
    """Test PaginatedResponse model."""

    def test_basic_response(self):
        """Test basic paginated response."""
        response = PaginatedResponse(
            items=[1, 2, 3],
            total=10,
            page=1,
            page_size=3,
            total_pages=4,
            has_next=True,
            has_prev=False
        )

        assert response.items == [1, 2, 3]
        assert response.total == 10
        assert response.page == 1
        assert response.total_pages == 4
        assert response.has_next is True
        assert response.has_prev is False

    def test_empty_response(self):
        """Test paginated response with no items."""
        response = PaginatedResponse(
            items=[],
            total=0,
            page=1,
            page_size=50,
            total_pages=0,
            has_next=False,
            has_prev=False
        )

        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0


@pytest.mark.unit
class TestPaginateFunction:
    """Test paginate utility function."""

    def test_first_page(self):
        """Test pagination of first page."""
        items = list(range(1, 11))  # 10 items
        total = 100  # Total 100 items
        params = PaginationParams(page=1, page_size=10)

        response = paginate(items, total, params)

        assert response.items == list(range(1, 11))
        assert response.total == 100
        assert response.page == 1
        assert response.page_size == 10
        assert response.total_pages == 10
        assert response.has_next is True
        assert response.has_prev is False

    def test_middle_page(self):
        """Test pagination of middle page."""
        items = list(range(51, 61))  # Items 51-60
        total = 100
        params = PaginationParams(page=6, page_size=10)

        response = paginate(items, total, params)

        assert response.page == 6
        assert response.has_next is True
        assert response.has_prev is True

    def test_last_page(self):
        """Test pagination of last page."""
        items = list(range(91, 101))  # Items 91-100
        total = 100
        params = PaginationParams(page=10, page_size=10)

        response = paginate(items, total, params)

        assert response.page == 10
        assert response.has_next is False
        assert response.has_prev is True

    def test_last_page_partial(self):
        """Test last page with fewer items than page_size."""
        items = list(range(91, 96))  # Only 5 items
        total = 95
        params = PaginationParams(page=10, page_size=10)

        response = paginate(items, total, params)

        assert len(response.items) == 5
        assert response.total_pages == 10
        assert response.has_next is False

    def test_single_page(self):
        """Test pagination when all items fit on one page."""
        items = list(range(1, 11))  # 10 items
        total = 10
        params = PaginationParams(page=1, page_size=50)

        response = paginate(items, total, params)

        assert response.total_pages == 1
        assert response.has_next is False
        assert response.has_prev is False

    def test_empty_results(self):
        """Test pagination with no results."""
        items = []
        total = 0
        params = PaginationParams(page=1, page_size=50)

        response = paginate(items, total, params)

        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_prev is False

    def test_total_pages_calculation(self):
        """Test total_pages calculation with various totals."""
        # Exact multiple
        params = PaginationParams(page=1, page_size=10)
        response = paginate([], 100, params)
        assert response.total_pages == 10

        # Remainder
        response = paginate([], 95, params)
        assert response.total_pages == 10

        # Less than one page
        response = paginate([], 5, params)
        assert response.total_pages == 1

        # Zero items
        response = paginate([], 0, params)
        assert response.total_pages == 0

    def test_generic_type_support(self):
        """Test pagination with different item types."""
        # Dictionary items
        dict_items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        params = PaginationParams(page=1, page_size=10)
        response = paginate(dict_items, 2, params)
        assert response.items == dict_items

        # String items
        string_items = ['a', 'b', 'c']
        response = paginate(string_items, 3, params)
        assert response.items == string_items


@pytest.mark.unit
class TestCreatePaginationParams:
    """Test create_pagination_params dependency function."""

    def test_default_params(self):
        """Test creating pagination params with defaults."""
        # Note: create_pagination_params is a FastAPI dependency and requires Query objects
        # We test PaginationParams directly instead
        params = PaginationParams()

        assert params.page == 1
        assert params.page_size == 50

    def test_custom_params(self):
        """Test creating pagination params with custom values."""
        params = PaginationParams(page=3, page_size=25)

        assert params.page == 3
        assert params.page_size == 25

    def test_invalid_params_raise_error(self):
        """Test that invalid params raise ValidationError."""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

        with pytest.raises(ValidationError):
            PaginationParams(page_size=0)

        with pytest.raises(ValidationError):
            PaginationParams(page_size=101)


@pytest.mark.unit
class TestPaginationEdgeCases:
    """Test edge cases in pagination."""

    def test_beyond_last_page(self):
        """Test requesting a page beyond the last page."""
        items = []  # No items for this page
        total = 100
        params = PaginationParams(page=20, page_size=10)  # Page 20 of 10

        response = paginate(items, total, params)

        assert response.items == []
        assert response.total_pages == 10
        assert response.page == 20
        assert response.has_next is False

    def test_very_large_page_number(self):
        """Test with very large page number."""
        items = []
        total = 100
        params = PaginationParams(page=1000, page_size=10)

        response = paginate(items, total, params)

        assert response.page == 1000
        assert response.total_pages == 10

    def test_page_size_one(self):
        """Test pagination with page_size=1."""
        items = [42]
        total = 100
        params = PaginationParams(page=42, page_size=1)

        response = paginate(items, total, params)

        assert response.items == [42]
        assert response.total_pages == 100
        assert response.has_next is True
        assert response.has_prev is True

    def test_total_less_than_page_size(self):
        """Test when total items is less than page_size."""
        items = [1, 2, 3]
        total = 3
        params = PaginationParams(page=1, page_size=50)

        response = paginate(items, total, params)

        assert response.total_pages == 1
        assert response.has_next is False
        assert response.has_prev is False


@pytest.mark.integration
class TestPaginationIntegration:
    """Integration tests for pagination with real-world scenarios."""

    def test_paginate_customer_list(self):
        """Test pagination of customer list."""
        # Simulate customer data
        customers = [
            {'customer_id': i, 'brand': f'Brand {i}'}
            for i in range(1, 26)  # 25 customers
        ]

        total = 100  # Total 100 customers in database
        params = PaginationParams(page=1, page_size=25)

        response = paginate(customers, total, params)

        assert len(response.items) == 25
        assert response.total == 100
        assert response.total_pages == 4
        assert response.has_next is True

    def test_sequential_page_navigation(self):
        """Test navigating through pages sequentially."""
        total = 100
        page_size = 10

        for page in range(1, 11):
            items = list(range((page - 1) * 10 + 1, page * 10 + 1))
            params = PaginationParams(page=page, page_size=page_size)
            response = paginate(items, total, params)

            assert response.page == page
            assert response.has_prev == (page > 1)
            assert response.has_next == (page < 10)

    def test_different_page_sizes(self):
        """Test pagination with different page sizes."""
        total = 100

        # Page size 10
        params = PaginationParams(page=1, page_size=10)
        response = paginate(list(range(10)), total, params)
        assert response.total_pages == 10

        # Page size 25
        params = PaginationParams(page=1, page_size=25)
        response = paginate(list(range(25)), total, params)
        assert response.total_pages == 4

        # Page size 50
        params = PaginationParams(page=1, page_size=50)
        response = paginate(list(range(50)), total, params)
        assert response.total_pages == 2

        # Page size 100
        params = PaginationParams(page=1, page_size=100)
        response = paginate(list(range(100)), total, params)
        assert response.total_pages == 1
