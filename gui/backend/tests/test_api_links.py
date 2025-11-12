"""
Integration tests for links API endpoints.

Tests:
- GET /api/v1/links (list all links)
- GET /api/v1/links/{id} (get specific link)
- Link filtering and search
- Pagination
- Error handling
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestLinksListEndpoint:
    """Test /api/v1/links endpoint."""

    def test_get_links_success(self, test_client):
        """Test successful retrieval of links."""
        response = test_client.get("/api/v1/links")

        assert response.status_code == 200
        data = response.json()

        assert 'items' in data
        assert 'total' in data
        assert 'page' in data
        assert isinstance(data['items'], list)

    def test_get_links_structure(self, test_client):
        """Test link data structure."""
        response = test_client.get("/api/v1/links")
        data = response.json()

        if len(data['items']) > 0:
            link = data['items'][0]
            assert 'id' in link
            assert 'customer_id' in link
            assert 'canonical_root' in link
            assert 'brand' in link
            assert 'pub_domain' in link
            assert 'target_url' in link
            assert 'anchor_text' in link
            assert 'published_at' in link

    def test_get_links_with_pagination(self, test_client):
        """Test links with pagination."""
        response = test_client.get("/api/v1/links?page=1&page_size=10")

        assert response.status_code == 200
        data = response.json()

        assert data['page'] == 1
        assert data['page_size'] == 10
        assert len(data['items']) <= 10

    def test_get_links_pagination_navigation(self, test_client):
        """Test pagination navigation indicators."""
        # First page
        response = test_client.get("/api/v1/links?page=1&page_size=2")
        data = response.json()

        assert data['has_prev'] is False
        if data['total'] > 2:
            assert data['has_next'] is True

    def test_get_links_with_date_range(self, test_client):
        """Test filtering links by date range."""
        response = test_client.get(
            "/api/v1/links?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        # Verify dates are within range
        for link in data['items']:
            published = link['published_at'][:7]  # YYYY-MM
            assert '2024-01' <= published <= '2024-03'

    def test_get_links_filter_by_customer(self, test_client):
        """Test filtering links by customer ID."""
        response = test_client.get("/api/v1/links?customer_id=1")

        assert response.status_code == 200
        data = response.json()

        # All links should be for customer 1
        for link in data['items']:
            assert link['customer_id'] == 1

    def test_get_links_filter_by_publisher(self, test_client):
        """Test filtering links by publisher domain."""
        response = test_client.get("/api/v1/links?pub_domain=blog.pub.com")

        assert response.status_code == 200
        data = response.json()

        # All links should be from specified publisher
        for link in data['items']:
            assert link['pub_domain'] == 'blog.pub.com'

    def test_get_links_search(self, test_client):
        """Test searching links by anchor text."""
        response = test_client.get("/api/v1/links?search=SEO")

        assert response.status_code == 200
        data = response.json()

        # Results should contain search term in anchor text or URL
        for link in data['items']:
            assert 'seo' in link['anchor_text'].lower() or \
                   'seo' in link['target_url'].lower()

    def test_get_links_combined_filters(self, test_client):
        """Test combining multiple filters."""
        response = test_client.get(
            "/api/v1/links?customer_id=1&from_date=2024-01&page_size=5"
        )

        assert response.status_code == 200
        data = response.json()

        # Verify all filters applied
        for link in data['items']:
            assert link['customer_id'] == 1
            assert link['published_at'][:7] >= '2024-01'


@pytest.mark.integration
class TestLinkDetailEndpoint:
    """Test /api/v1/links/{id} endpoint."""

    def test_get_link_by_id_success(self, test_client):
        """Test retrieving specific link by ID."""
        # First, get a link ID from the list
        list_response = test_client.get("/api/v1/links?page_size=1")
        links = list_response.json()['items']

        if len(links) > 0:
            link_id = links[0]['id']

            # Get specific link
            response = test_client.get(f"/api/v1/links/{link_id}")

            assert response.status_code == 200
            data = response.json()

            assert data['id'] == link_id

    def test_get_link_by_id_structure(self, test_client):
        """Test detailed link data structure."""
        # Get any link
        list_response = test_client.get("/api/v1/links?page_size=1")
        links = list_response.json()['items']

        if len(links) > 0:
            link_id = links[0]['id']
            response = test_client.get(f"/api/v1/links/{link_id}")
            data = response.json()

            # Check all fields present
            assert 'id' in data
            assert 'customer_id' in data
            assert 'pub_domain' in data
            assert 'target_url' in data
            assert 'anchor_text' in data
            assert 'published_at' in data
            assert 'inserted_at' in data

    def test_get_link_nonexistent_id(self, test_client):
        """Test retrieving non-existent link."""
        response = test_client.get("/api/v1/links/99999")

        assert response.status_code == 404

    def test_get_link_invalid_id(self, test_client):
        """Test with invalid link ID format."""
        response = test_client.get("/api/v1/links/abc")

        assert response.status_code == 422


@pytest.mark.integration
class TestLinksSorting:
    """Test sorting functionality for links."""

    def test_links_sorted_by_date_desc(self, test_client):
        """Test default sorting (most recent first)."""
        response = test_client.get("/api/v1/links?page_size=10")
        data = response.json()

        if len(data['items']) > 1:
            dates = [link['published_at'] for link in data['items']]
            assert dates == sorted(dates, reverse=True)

    def test_links_sorted_by_date_asc(self, test_client):
        """Test sorting by date ascending."""
        response = test_client.get("/api/v1/links?sort=date_asc&page_size=10")

        if response.status_code == 200:
            data = response.json()
            if len(data['items']) > 1:
                dates = [link['published_at'] for link in data['items']]
                assert dates == sorted(dates)

    def test_links_sorted_by_domain(self, test_client):
        """Test sorting by publisher domain."""
        response = test_client.get("/api/v1/links?sort=domain&page_size=10")

        if response.status_code == 200:
            data = response.json()
            if len(data['items']) > 1:
                domains = [link['pub_domain'] for link in data['items']]
                assert domains == sorted(domains)


@pytest.mark.integration
@pytest.mark.security
class TestLinksSecurityValidation:
    """Test security validation for links endpoints."""

    def test_sql_injection_in_search(self, test_client):
        """Test SQL injection prevention in search."""
        response = test_client.get(
            "/api/v1/links?search='; DROP TABLE customer_history; --"
        )

        # Should be rejected by validation
        assert response.status_code == 422

    def test_xss_in_search(self, test_client):
        """Test XSS prevention in search."""
        response = test_client.get(
            "/api/v1/links?search=<script>alert('xss')</script>"
        )

        # Should either reject or sanitize
        if response.status_code == 200:
            data = response.json()
            # Verify no script tags in response
            for link in data['items']:
                assert '<script>' not in link['anchor_text']

    def test_invalid_customer_id_type(self, test_client):
        """Test type validation for customer_id filter."""
        response = test_client.get("/api/v1/links?customer_id=abc")

        assert response.status_code == 422

    def test_negative_customer_id(self, test_client):
        """Test negative customer_id is rejected."""
        response = test_client.get("/api/v1/links?customer_id=-1")

        assert response.status_code == 422


@pytest.mark.integration
class TestLinksPerformance:
    """Performance tests for links endpoints."""

    @pytest.mark.performance
    def test_links_list_performance(self, test_client):
        """Test links list response time."""
        import time

        start = time.time()
        response = test_client.get("/api/v1/links?page_size=50")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should respond quickly

    @pytest.mark.performance
    def test_links_with_filters_performance(self, test_client):
        """Test performance with multiple filters."""
        import time

        start = time.time()
        response = test_client.get(
            "/api/v1/links?customer_id=1&from_date=2024-01&page_size=50"
        )
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Indexes should make this fast

    @pytest.mark.performance
    def test_links_search_performance(self, test_client):
        """Test search performance."""
        import time

        start = time.time()
        response = test_client.get("/api/v1/links?search=SEO&page_size=50")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 2.0  # Search may be slower but should be reasonable

    @pytest.mark.performance
    def test_deep_pagination_performance(self, test_client):
        """Test that deep pagination doesn't degrade too much."""
        import time

        # First page
        start = time.time()
        response1 = test_client.get("/api/v1/links?page=1&page_size=10")
        duration1 = time.time() - start

        # Deep page
        start = time.time()
        response2 = test_client.get("/api/v1/links?page=10&page_size=10")
        duration2 = time.time() - start

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Performance should not degrade significantly
        assert duration2 < duration1 * 3


@pytest.mark.integration
class TestLinksCaching:
    """Test caching behavior for links endpoints."""

    def test_links_list_cached(self, test_client):
        """Test that links list is cached."""
        import time

        # First request
        start = time.time()
        response1 = test_client.get("/api/v1/links?page=1&page_size=10")
        duration1 = time.time() - start

        # Second request - should be cached
        start = time.time()
        response2 = test_client.get("/api/v1/links?page=1&page_size=10")
        duration2 = time.time() - start

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Cached should be faster
        assert duration2 < duration1 / 2

    def test_different_filters_different_cache(self, test_client):
        """Test that different filters create different cache entries."""
        response1 = test_client.get("/api/v1/links?customer_id=1")
        response2 = test_client.get("/api/v1/links?customer_id=2")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Should return different results
        data1 = response1.json()
        data2 = response2.json()

        if data1['total'] > 0 and data2['total'] > 0:
            assert data1['items'][0]['customer_id'] != data2['items'][0]['customer_id']


@pytest.mark.integration
class TestLinksErrorHandling:
    """Test error handling for links endpoints."""

    def test_invalid_date_format(self, test_client):
        """Test with invalid date format."""
        response = test_client.get("/api/v1/links?from_date=2024/01/01")

        assert response.status_code == 422

    def test_invalid_page_number(self, test_client):
        """Test with invalid page number."""
        response = test_client.get("/api/v1/links?page=0")
        assert response.status_code == 422

        response = test_client.get("/api/v1/links?page=-1")
        assert response.status_code == 422

    def test_invalid_page_size(self, test_client):
        """Test with invalid page size."""
        response = test_client.get("/api/v1/links?page_size=0")
        assert response.status_code == 422

        response = test_client.get("/api/v1/links?page_size=101")
        assert response.status_code == 422

    def test_malformed_query_parameters(self, test_client):
        """Test with malformed query parameters."""
        response = test_client.get("/api/v1/links?customer_id=not_a_number")

        assert response.status_code == 422


@pytest.mark.integration
class TestLinksDataValidation:
    """Test data validation in links responses."""

    def test_all_links_have_required_fields(self, test_client):
        """Test that all returned links have required fields."""
        response = test_client.get("/api/v1/links?page_size=50")
        data = response.json()

        required_fields = [
            'id', 'customer_id', 'canonical_root', 'brand',
            'pub_domain', 'target_url', 'anchor_text', 'published_at'
        ]

        for link in data['items']:
            for field in required_fields:
                assert field in link
                assert link[field] is not None

    def test_urls_are_valid(self, test_client):
        """Test that URLs in responses are valid."""
        response = test_client.get("/api/v1/links?page_size=10")
        data = response.json()

        for link in data['items']:
            # target_url should start with http:// or https://
            assert link['target_url'].startswith('http://') or \
                   link['target_url'].startswith('https://')

    def test_dates_are_valid_format(self, test_client):
        """Test that dates are in valid ISO format."""
        response = test_client.get("/api/v1/links?page_size=10")
        data = response.json()

        import re
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')

        for link in data['items']:
            assert date_pattern.match(link['published_at'])
            assert date_pattern.match(link['inserted_at'])
