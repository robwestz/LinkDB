"""
Integration tests for customer API endpoints.

Tests:
- GET /api/v1/customers (list all customers)
- GET /api/v1/customers/{customer_id}/links (get customer links)
- GET /api/v1/customers/{customer_id}/stats (get customer statistics)
- Pagination
- Error handling
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestCustomersEndpoint:
    """Test /api/v1/customers endpoint."""

    def test_get_customers_success(self, test_client):
        """Test successful retrieval of customers."""
        response = test_client.get("/api/v1/customers")

        assert response.status_code == 200
        data = response.json()

        assert 'items' in data
        assert 'total' in data
        assert 'page' in data
        assert isinstance(data['items'], list)

    def test_get_customers_structure(self, test_client):
        """Test customer data structure."""
        response = test_client.get("/api/v1/customers")
        data = response.json()

        if len(data['items']) > 0:
            customer = data['items'][0]
            assert 'customer_id' in customer
            assert 'canonical_root' in customer
            assert 'brand' in customer
            assert 'total_links' in customer

    def test_get_customers_with_pagination(self, test_client):
        """Test customers endpoint with pagination."""
        response = test_client.get("/api/v1/customers?page=1&page_size=10")

        assert response.status_code == 200
        data = response.json()

        assert data['page'] == 1
        assert data['page_size'] == 10
        assert len(data['items']) <= 10

    def test_get_customers_page_2(self, test_client):
        """Test getting second page of customers."""
        response = test_client.get("/api/v1/customers?page=2&page_size=1")

        assert response.status_code == 200
        data = response.json()

        assert data['page'] == 2
        assert data['has_prev'] is True

    def test_get_customers_invalid_page(self, test_client):
        """Test with invalid page number."""
        response = test_client.get("/api/v1/customers?page=0")

        assert response.status_code == 422  # Validation error

    def test_get_customers_invalid_page_size(self, test_client):
        """Test with invalid page size."""
        response = test_client.get("/api/v1/customers?page_size=0")
        assert response.status_code == 422

        response = test_client.get("/api/v1/customers?page_size=101")
        assert response.status_code == 422


@pytest.mark.integration
class TestCustomerLinksEndpoint:
    """Test /api/v1/customers/{customer_id}/links endpoint."""

    def test_get_customer_links_success(self, test_client):
        """Test successful retrieval of customer links."""
        # Using customer_id from test data
        response = test_client.get("/api/v1/customers/1/links")

        assert response.status_code == 200
        data = response.json()

        assert 'items' in data
        assert 'total' in data
        assert isinstance(data['items'], list)

    def test_get_customer_links_structure(self, test_client):
        """Test link data structure."""
        response = test_client.get("/api/v1/customers/1/links")
        data = response.json()

        if len(data['items']) > 0:
            link = data['items'][0]
            assert 'id' in link
            assert 'pub_domain' in link
            assert 'target_url' in link
            assert 'anchor_text' in link
            assert 'published_at' in link

    def test_get_customer_links_with_pagination(self, test_client):
        """Test customer links with pagination."""
        response = test_client.get("/api/v1/customers/1/links?page=1&page_size=5")

        assert response.status_code == 200
        data = response.json()

        assert data['page'] == 1
        assert data['page_size'] == 5
        assert len(data['items']) <= 5

    def test_get_customer_links_with_date_range(self, test_client):
        """Test filtering links by date range."""
        response = test_client.get(
            "/api/v1/customers/1/links?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        # Verify dates are within range
        for link in data['items']:
            published = link['published_at'][:7]  # YYYY-MM
            assert '2024-01' <= published <= '2024-03'

    def test_get_customer_links_invalid_customer(self, test_client):
        """Test with non-existent customer ID."""
        response = test_client.get("/api/v1/customers/99999/links")

        # Should return empty result, not error
        assert response.status_code == 200
        data = response.json()
        assert data['total'] == 0

    def test_get_customer_links_negative_customer_id(self, test_client):
        """Test with negative customer ID."""
        response = test_client.get("/api/v1/customers/-1/links")

        assert response.status_code == 422  # Validation error

    def test_get_customer_links_invalid_date_format(self, test_client):
        """Test with invalid date format."""
        response = test_client.get(
            "/api/v1/customers/1/links?from_date=2024/01"
        )

        assert response.status_code == 422


@pytest.mark.integration
class TestCustomerStatsEndpoint:
    """Test /api/v1/customers/{customer_id}/stats endpoint."""

    def test_get_customer_stats_success(self, test_client):
        """Test successful retrieval of customer statistics."""
        response = test_client.get("/api/v1/customers/1/stats")

        assert response.status_code == 200
        data = response.json()

        assert 'customer_id' in data
        assert 'total_links' in data
        assert 'unique_publishers' in data
        assert 'date_range' in data

    def test_get_customer_stats_structure(self, test_client):
        """Test stats data structure."""
        response = test_client.get("/api/v1/customers/1/stats")
        data = response.json()

        assert isinstance(data['total_links'], int)
        assert isinstance(data['unique_publishers'], int)
        assert isinstance(data['date_range'], dict)
        assert 'first_published' in data['date_range']
        assert 'last_published' in data['date_range']

    def test_get_customer_stats_with_date_range(self, test_client):
        """Test stats with date range filter."""
        response = test_client.get(
            "/api/v1/customers/1/stats?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        assert 'total_links' in data

    def test_get_customer_stats_invalid_customer(self, test_client):
        """Test stats for non-existent customer."""
        response = test_client.get("/api/v1/customers/99999/stats")

        assert response.status_code == 200
        data = response.json()
        assert data['total_links'] == 0


@pytest.mark.integration
class TestCustomerSearchEndpoint:
    """Test customer search functionality."""

    def test_search_customers_by_brand(self, test_client):
        """Test searching customers by brand name."""
        response = test_client.get("/api/v1/customers?search=Example")

        assert response.status_code == 200
        data = response.json()

        # Results should contain search term
        for customer in data['items']:
            assert 'example' in customer['brand'].lower() or \
                   'example' in customer['canonical_root'].lower()

    def test_search_customers_case_insensitive(self, test_client):
        """Test search is case insensitive by default."""
        response1 = test_client.get("/api/v1/customers?search=example")
        response2 = test_client.get("/api/v1/customers?search=EXAMPLE")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Should return same results
        data1 = response1.json()
        data2 = response2.json()
        assert data1['total'] == data2['total']

    def test_search_customers_sql_injection_prevention(self, test_client):
        """Test SQL injection prevention in search."""
        response = test_client.get(
            "/api/v1/customers?search='; DROP TABLE customer_history; --"
        )

        # Should be rejected by validation
        assert response.status_code == 422


@pytest.mark.integration
class TestCustomerCachingBehavior:
    """Test caching behavior for customer endpoints."""

    def test_customers_endpoint_cached(self, test_client):
        """Test that customers endpoint responses are cached."""
        # First request
        response1 = test_client.get("/api/v1/customers")
        assert response1.status_code == 200

        # Second request - should be faster (cached)
        import time
        start = time.time()
        response2 = test_client.get("/api/v1/customers")
        duration = time.time() - start

        assert response2.status_code == 200
        assert duration < 0.1  # Cached response should be very fast

    def test_cache_invalidation_after_update(self, test_client):
        """Test that cache is invalidated after data updates."""
        # Get initial data
        response1 = test_client.get("/api/v1/customers/1/stats")
        initial_count = response1.json()['total_links']

        # Add a new link (assuming CRUD endpoint exists)
        # This would invalidate the cache
        # TODO: Implement once CRUD endpoints are ready

        # Get updated data
        response2 = test_client.get("/api/v1/customers/1/stats")
        # Should reflect changes (not cached old data)


@pytest.mark.integration
class TestCustomerErrorHandling:
    """Test error handling for customer endpoints."""

    def test_malformed_customer_id(self, test_client):
        """Test with malformed customer ID."""
        response = test_client.get("/api/v1/customers/abc/links")

        assert response.status_code == 422  # Validation error

    def test_very_large_customer_id(self, test_client):
        """Test with unreasonably large customer ID."""
        response = test_client.get("/api/v1/customers/99999999/links")

        # Should be rejected by validation
        assert response.status_code == 422

    def test_missing_required_parameters(self, test_client):
        """Test endpoints with missing parameters."""
        # All customer endpoints should have customer_id in path
        # So this should 404
        response = test_client.get("/api/v1/customers//links")

        assert response.status_code in [404, 422]


@pytest.mark.integration
class TestCustomerPerformance:
    """Performance tests for customer endpoints."""

    @pytest.mark.performance
    def test_customers_endpoint_performance(self, test_client):
        """Test customers endpoint response time."""
        import time

        start = time.time()
        response = test_client.get("/api/v1/customers")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should respond in under 1 second

    @pytest.mark.performance
    def test_customer_links_with_large_dataset(self, benchmark_db, test_client):
        """Test performance with large dataset."""
        import time

        # Assuming benchmark_db has 1000 records
        start = time.time()
        response = test_client.get("/api/v1/customers/1/links?page_size=100")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 2.0  # Should handle large queries efficiently

    @pytest.mark.performance
    def test_pagination_performance(self, test_client):
        """Test pagination doesn't degrade with higher page numbers."""
        import time

        # Test first page
        start = time.time()
        response1 = test_client.get("/api/v1/customers?page=1&page_size=10")
        duration1 = time.time() - start

        # Test later page
        start = time.time()
        response2 = test_client.get("/api/v1/customers?page=5&page_size=10")
        duration2 = time.time() - start

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Performance should be similar
        assert abs(duration1 - duration2) < 0.5
