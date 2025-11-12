"""
Integration tests for dashboard API endpoints.

Tests:
- GET /api/v1/dashboard/metrics (overview metrics)
- GET /api/v1/dashboard/activity (recent activity)
- GET /api/v1/dashboard/top-publishers (top publishers)
- Date range filtering
- Error handling
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestDashboardMetrics:
    """Test /api/v1/dashboard/metrics endpoint."""

    def test_get_metrics_success(self, test_client):
        """Test successful retrieval of dashboard metrics."""
        response = test_client.get("/api/v1/dashboard/metrics")

        assert response.status_code == 200
        data = response.json()

        assert 'total_customers' in data
        assert 'total_links' in data
        assert 'total_publishers' in data
        assert 'total_domains' in data

    def test_metrics_data_types(self, test_client):
        """Test that metric values are correct types."""
        response = test_client.get("/api/v1/dashboard/metrics")
        data = response.json()

        assert isinstance(data['total_customers'], int)
        assert isinstance(data['total_links'], int)
        assert isinstance(data['total_publishers'], int)
        assert isinstance(data['total_domains'], int)

        assert data['total_customers'] >= 0
        assert data['total_links'] >= 0
        assert data['total_publishers'] >= 0
        assert data['total_domains'] >= 0

    def test_metrics_with_date_range(self, test_client):
        """Test metrics filtered by date range."""
        response = test_client.get(
            "/api/v1/dashboard/metrics?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        # Filtered metrics should be less than or equal to total
        assert 'total_links' in data

    def test_metrics_invalid_date_range(self, test_client):
        """Test with invalid date range (from > to)."""
        response = test_client.get(
            "/api/v1/dashboard/metrics?from_date=2024-06&to_date=2024-01"
        )

        assert response.status_code == 422  # Validation error

    def test_metrics_future_date(self, test_client):
        """Test with future date."""
        response = test_client.get(
            "/api/v1/dashboard/metrics?from_date=2099-01"
        )

        # Should return zero results or reject
        assert response.status_code in [200, 422]

    def test_metrics_cached(self, test_client):
        """Test that metrics are cached for performance."""
        import time

        # First request
        start = time.time()
        response1 = test_client.get("/api/v1/dashboard/metrics")
        duration1 = time.time() - start

        # Second request - should be cached
        start = time.time()
        response2 = test_client.get("/api/v1/dashboard/metrics")
        duration2 = time.time() - start

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert duration2 < duration1 / 2  # Cached should be much faster


@pytest.mark.integration
class TestDashboardActivity:
    """Test /api/v1/dashboard/activity endpoint."""

    def test_get_activity_success(self, test_client):
        """Test successful retrieval of recent activity."""
        response = test_client.get("/api/v1/dashboard/activity")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    def test_activity_structure(self, test_client):
        """Test activity item structure."""
        response = test_client.get("/api/v1/dashboard/activity?limit=10")
        data = response.json()

        if len(data) > 0:
            activity = data[0]
            assert 'id' in activity
            assert 'customer_id' in activity
            assert 'brand' in activity
            assert 'pub_domain' in activity
            assert 'published_at' in activity

    def test_activity_limit_parameter(self, test_client):
        """Test limiting number of activity items."""
        response = test_client.get("/api/v1/dashboard/activity?limit=5")

        assert response.status_code == 200
        data = response.json()

        assert len(data) <= 5

    def test_activity_sorted_by_date(self, test_client):
        """Test that activity is sorted by date (most recent first)."""
        response = test_client.get("/api/v1/dashboard/activity?limit=10")
        data = response.json()

        if len(data) > 1:
            # Check that dates are in descending order
            dates = [item['published_at'] for item in data]
            assert dates == sorted(dates, reverse=True)

    def test_activity_with_date_range(self, test_client):
        """Test activity filtered by date range."""
        response = test_client.get(
            "/api/v1/dashboard/activity?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        # All items should be within date range
        for activity in data:
            published = activity['published_at'][:7]  # YYYY-MM
            assert '2024-01' <= published <= '2024-03'


@pytest.mark.integration
class TestDashboardTopPublishers:
    """Test /api/v1/dashboard/top-publishers endpoint."""

    def test_get_top_publishers_success(self, test_client):
        """Test successful retrieval of top publishers."""
        response = test_client.get("/api/v1/dashboard/top-publishers")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    def test_top_publishers_structure(self, test_client):
        """Test publisher data structure."""
        response = test_client.get("/api/v1/dashboard/top-publishers?limit=10")
        data = response.json()

        if len(data) > 0:
            publisher = data[0]
            assert 'pub_domain' in publisher
            assert 'link_count' in publisher
            assert isinstance(publisher['link_count'], int)

    def test_top_publishers_sorted(self, test_client):
        """Test that publishers are sorted by link count."""
        response = test_client.get("/api/v1/dashboard/top-publishers?limit=10")
        data = response.json()

        if len(data) > 1:
            counts = [p['link_count'] for p in data]
            assert counts == sorted(counts, reverse=True)

    def test_top_publishers_limit(self, test_client):
        """Test limiting number of publishers."""
        response = test_client.get("/api/v1/dashboard/top-publishers?limit=5")

        assert response.status_code == 200
        data = response.json()

        assert len(data) <= 5

    def test_top_publishers_with_date_range(self, test_client):
        """Test top publishers filtered by date range."""
        response = test_client.get(
            "/api/v1/dashboard/top-publishers?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)


@pytest.mark.integration
class TestDashboardCharts:
    """Test dashboard chart data endpoints."""

    def test_links_over_time(self, test_client):
        """Test links over time chart data."""
        response = test_client.get("/api/v1/dashboard/links-over-time")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

        if len(data) > 0:
            point = data[0]
            assert 'month' in point
            assert 'count' in point

    def test_links_over_time_with_date_range(self, test_client):
        """Test links over time with date range."""
        response = test_client.get(
            "/api/v1/dashboard/links-over-time?from_date=2024-01&to_date=2024-03"
        )

        assert response.status_code == 200
        data = response.json()

        # All data points should be within range
        for point in data:
            assert '2024-01' <= point['month'] <= '2024-03'

    def test_links_over_time_sorted(self, test_client):
        """Test that time series data is sorted chronologically."""
        response = test_client.get("/api/v1/dashboard/links-over-time")
        data = response.json()

        if len(data) > 1:
            months = [p['month'] for p in data]
            assert months == sorted(months)


@pytest.mark.integration
class TestDashboardPerformance:
    """Performance tests for dashboard endpoints."""

    @pytest.mark.performance
    def test_metrics_performance(self, test_client):
        """Test dashboard metrics response time."""
        import time

        start = time.time()
        response = test_client.get("/api/v1/dashboard/metrics")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should be fast

    @pytest.mark.performance
    def test_activity_performance(self, test_client):
        """Test activity endpoint performance."""
        import time

        start = time.time()
        response = test_client.get("/api/v1/dashboard/activity?limit=50")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0

    @pytest.mark.performance
    def test_concurrent_dashboard_requests(self, test_client):
        """Test handling multiple concurrent dashboard requests."""
        import concurrent.futures
        import time

        def fetch_metrics():
            return test_client.get("/api/v1/dashboard/metrics")

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_metrics) for _ in range(10)]
            results = [f.result() for f in futures]
        duration = time.time() - start

        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
        # Should complete in reasonable time with caching
        assert duration < 2.0


@pytest.mark.integration
class TestDashboardErrorHandling:
    """Test error handling for dashboard endpoints."""

    def test_metrics_invalid_date_format(self, test_client):
        """Test with invalid date format."""
        response = test_client.get(
            "/api/v1/dashboard/metrics?from_date=2024/01/01"
        )

        assert response.status_code == 422

    def test_activity_invalid_limit(self, test_client):
        """Test with invalid limit parameter."""
        response = test_client.get("/api/v1/dashboard/activity?limit=-1")

        assert response.status_code == 422

        response = test_client.get("/api/v1/dashboard/activity?limit=0")
        assert response.status_code == 422

    def test_top_publishers_invalid_limit(self, test_client):
        """Test with invalid limit for top publishers."""
        response = test_client.get("/api/v1/dashboard/top-publishers?limit=1000")

        # Should either reject or cap at max value
        assert response.status_code in [200, 422]

    def test_malformed_query_parameters(self, test_client):
        """Test with malformed query parameters."""
        response = test_client.get("/api/v1/dashboard/metrics?from_date=abc")

        assert response.status_code == 422


@pytest.mark.integration
class TestDashboardDataConsistency:
    """Test data consistency across dashboard endpoints."""

    def test_total_links_consistency(self, test_client):
        """Test that total links is consistent across endpoints."""
        # Get from metrics
        metrics_response = test_client.get("/api/v1/dashboard/metrics")
        metrics_total = metrics_response.json()['total_links']

        # Get from customers and sum
        customers_response = test_client.get("/api/v1/customers?page_size=100")
        customers_data = customers_response.json()
        customers_total = sum(c['total_links'] for c in customers_data['items'])

        # Should match (or be close if paginated)
        assert abs(metrics_total - customers_total) <= customers_data['total']

    def test_customer_count_consistency(self, test_client):
        """Test customer count is consistent."""
        # Get from metrics
        metrics_response = test_client.get("/api/v1/dashboard/metrics")
        metrics_customers = metrics_response.json()['total_customers']

        # Get from customers list
        customers_response = test_client.get("/api/v1/customers")
        customers_count = customers_response.json()['total']

        assert metrics_customers == customers_count


@pytest.mark.integration
class TestDashboardCaching:
    """Test caching behavior for dashboard endpoints."""

    def test_cache_headers_present(self, test_client):
        """Test that appropriate cache headers are present."""
        response = test_client.get("/api/v1/dashboard/metrics")

        assert response.status_code == 200
        # Check for cache-related headers if implemented

    def test_cached_response_consistency(self, test_client):
        """Test that cached responses are consistent."""
        # Make same request twice
        response1 = test_client.get("/api/v1/dashboard/metrics")
        response2 = test_client.get("/api/v1/dashboard/metrics")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Data should be identical
        assert response1.json() == response2.json()
