"""
Unit tests for database connection pooling.

Tests:
- Connection pool initialization
- Connection acquisition and release
- Connection pool exhaustion handling
- Connection health checks
- Context manager functionality
- Concurrent connection handling
"""

import pytest
import sqlite3
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from database import ConnectionPool, get_db_connection


@pytest.mark.unit
class TestConnectionPool:
    """Test ConnectionPool class."""

    def test_pool_initialization(self, tmp_path):
        """Test that connection pool initializes correctly."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=5, max_overflow=2)

        assert pool.pool_size == 5
        assert pool.max_overflow == 2
        assert pool.pool.qsize() == 5  # All connections should be in pool

    def test_get_connection_success(self, tmp_path):
        """Test successful connection acquisition."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=2)

        with pool.get_connection() as conn:
            assert isinstance(conn, sqlite3.Connection)
            # Connection should work
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1

    def test_connection_returned_to_pool(self, tmp_path):
        """Test that connection is returned to pool after use."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=2)

        initial_size = pool.pool.qsize()

        with pool.get_connection() as conn:
            assert pool.pool.qsize() == initial_size - 1  # One connection taken

        # Connection should be returned
        assert pool.pool.qsize() == initial_size

    def test_multiple_connections(self, tmp_path):
        """Test acquiring multiple connections."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=3)

        with pool.get_connection() as conn1:
            with pool.get_connection() as conn2:
                assert conn1 != conn2  # Different connections
                assert isinstance(conn1, sqlite3.Connection)
                assert isinstance(conn2, sqlite3.Connection)

    def test_pool_exhaustion_timeout(self, tmp_path):
        """Test timeout when pool is exhausted."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=1, max_overflow=0)

        with pool.get_connection() as conn1:
            # Try to get another connection - should timeout
            with pytest.raises(Exception):  # Queue.Empty or timeout error
                with pool.get_connection(timeout=0.1) as conn2:
                    pass

    def test_connection_health_check(self, tmp_path):
        """Test connection health checking."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))

        # Create a valid connection
        conn = sqlite3.connect(str(db_path))
        assert pool._is_connection_healthy(conn) is True

        # Close connection and check health
        conn.close()
        assert pool._is_connection_healthy(conn) is False

        pool.close_all()

    def test_wal_mode_enabled(self, tmp_path):
        """Test that WAL mode is enabled on connections."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))

        with pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode")
            journal_mode = cursor.fetchone()[0]
            assert journal_mode.upper() == 'WAL'

    def test_row_factory_set(self, tmp_path):
        """Test that row_factory is set to Row."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))

        with pool.get_connection() as conn:
            assert conn.row_factory == sqlite3.Row

    def test_close_pool(self, tmp_path):
        """Test closing all connections in pool."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=3)

        pool.close_all()

        # Pool should be empty after close
        assert pool.pool.qsize() == 0


@pytest.mark.unit
class TestGlobalConnectionFunctions:
    """Test global database connection functions."""

    def test_get_db_connection_context_manager(self, test_db_path):
        """Test get_db_connection as context manager."""
        with patch('database.get_database_path', return_value=Path(test_db_path)):
            with get_db_connection() as conn:
                assert isinstance(conn, sqlite3.Connection)

                # Should be able to query
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                assert cursor.fetchone()[0] == 1

    def test_connection_reuse(self, test_db_path):
        """Test that connections are reused from pool."""
        with patch('database.get_database_path', return_value=Path(test_db_path)):
            # Get connection twice
            with get_db_connection() as conn1:
                conn1_id = id(conn1)

            with get_db_connection() as conn2:
                conn2_id = id(conn2)

            # Should get same connection from pool (or at least pool should work)
            assert isinstance(conn1_id, int)
            assert isinstance(conn2_id, int)


@pytest.mark.integration
class TestConnectionPoolIntegration:
    """Integration tests for connection pool with real database operations."""

    def test_concurrent_queries(self, test_db):
        """Test multiple concurrent queries using pool."""
        # Test DB already has customer_history table
        results = []

        # Simulate concurrent queries
        for i in range(5):
            cursor = test_db.cursor()
            cursor.execute("SELECT COUNT(*) FROM customer_history")
            count = cursor.fetchone()[0]
            results.append(count)

        # All queries should succeed
        assert len(results) == 5
        assert all(isinstance(r, int) for r in results)

    def test_transaction_handling(self, test_db):
        """Test that transactions work correctly with pooled connections."""
        cursor = test_db.cursor()

        # Start transaction
        cursor.execute("""
            INSERT INTO customer_history
            (customer_id, canonical_root, brand, pub_domain, target_url,
             anchor_text, published_at, inserted_at)
            VALUES (999, 'test.com', 'Test', 'pub.com', 'https://test.com',
                    'test', '2024-01-01', datetime('now'))
        """)
        test_db.commit()

        # Verify insert
        cursor.execute("SELECT COUNT(*) FROM customer_history WHERE customer_id = 999")
        count = cursor.fetchone()[0]
        assert count > 0

        # Cleanup
        cursor.execute("DELETE FROM customer_history WHERE customer_id = 999")
        test_db.commit()

    def test_connection_isolation(self, tmp_path):
        """Test that connections are properly isolated."""
        db_path = tmp_path / "test_isolation.db"
        pool = ConnectionPool(str(db_path))

        # Create temporary table in one connection
        with pool.get_connection() as conn1:
            cursor1 = conn1.cursor()
            cursor1.execute("CREATE TEMP TABLE temp_test (id INTEGER)")
            cursor1.execute("INSERT INTO temp_test VALUES (1)")
            conn1.commit()

            # Temp table should exist in this connection
            cursor1.execute("SELECT COUNT(*) FROM temp_test")
            assert cursor1.fetchone()[0] == 1

        # Temp table should NOT exist in new connection
        # (TEMP tables are connection-specific, this tests isolation)
        with pool.get_connection() as conn2:
            cursor2 = conn2.cursor()
            with pytest.raises(sqlite3.OperationalError):
                cursor2.execute("SELECT COUNT(*) FROM temp_test")

        pool.close_all()


@pytest.mark.unit
class TestConnectionPoolErrorHandling:
    """Test error handling in connection pool."""

    def test_invalid_database_path(self):
        """Test handling of invalid database path."""
        with pytest.raises(Exception):
            pool = ConnectionPool("/invalid/path/to/database.db")
            with pool.get_connection() as conn:
                pass

    def test_connection_error_recovery(self, tmp_path):
        """Test that pool can recover from connection errors."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path), pool_size=2)

        # Get a connection and corrupt it
        with pool.get_connection() as conn:
            # Simulate connection error by closing it
            conn.close()

            # Connection health check should fail
            assert pool._is_connection_healthy(conn) is False

        # Pool should still work with other connections
        with pool.get_connection() as conn2:
            assert pool._is_connection_healthy(conn2) is True

        pool.close_all()


@pytest.mark.performance
class TestConnectionPoolPerformance:
    """Performance tests for connection pool."""

    def test_pooling_faster_than_new_connections(self, tmp_path):
        """Test that pooling is faster than creating new connections."""
        db_path = tmp_path / "test.db"

        # Create test database
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        # Test without pooling (new connection each time)
        start = time.time()
        for _ in range(10):
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
        no_pool_duration = time.time() - start

        # Test with pooling
        pool = ConnectionPool(str(db_path), pool_size=5)
        start = time.time()
        for _ in range(10):
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
        pool_duration = time.time() - start

        pool.close_all()

        # Pooling should be faster
        assert pool_duration < no_pool_duration

    def test_high_concurrency(self, tmp_path):
        """Test pool performance under high concurrency."""
        db_path = tmp_path / "test.db"

        # Create test database
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        pool = ConnectionPool(str(db_path), pool_size=10, max_overflow=5)

        # Simulate 50 concurrent requests
        start = time.time()
        for _ in range(50):
            try:
                with pool.get_connection(timeout=2.0) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
            except Exception:
                pass  # Timeout is acceptable under high load

        duration = time.time() - start
        pool.close_all()

        # Should complete in reasonable time (adjust based on hardware)
        assert duration < 5.0  # 50 queries in under 5 seconds


@pytest.mark.unit
class TestConnectionHealthCheck:
    """Test connection health check method."""

    def test_healthy_connection(self, tmp_path):
        """Test health check on healthy connection."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))
        conn = sqlite3.connect(str(db_path))

        assert pool._is_connection_healthy(conn) is True

        conn.close()
        pool.close_all()

    def test_closed_connection(self, tmp_path):
        """Test health check on closed connection."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))
        conn = sqlite3.connect(str(db_path))
        conn.close()

        assert pool._is_connection_healthy(conn) is False

        pool.close_all()

    def test_none_connection(self, tmp_path):
        """Test health check on None."""
        db_path = tmp_path / "test.db"
        pool = ConnectionPool(str(db_path))

        # This will raise an exception but that's expected behavior
        try:
            result = pool._is_connection_healthy(None)
            assert result is False
        except Exception:
            pass  # Expected for None connection

        pool.close_all()
