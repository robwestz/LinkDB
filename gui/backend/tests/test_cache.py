"""
Unit tests for cache module.

Tests:
- Cache initialization
- Key generation
- Get/set/delete operations
- TTL expiration
- Decorator functionality
- Cache statistics
- Cache invalidation
"""

import pytest
import time
from unittest.mock import patch
from cache import (
    ResponseCache,
    cached,
    get_cache_stats,
    clear_cache,
    invalidate_customer_cache
)


@pytest.mark.unit
class TestResponseCache:
    """Test ResponseCache class."""

    def test_cache_initialization(self):
        """Test cache is initialized with correct parameters."""
        cache = ResponseCache(maxsize=50, ttl=60)
        assert cache.ttl == 60
        assert cache.hits == 0
        assert cache.misses == 0

    def test_generate_key_consistency(self):
        """Test that same arguments generate same key."""
        cache = ResponseCache()

        key1 = cache.generate_key(1, 2, 3, foo='bar', baz='qux')
        key2 = cache.generate_key(1, 2, 3, foo='bar', baz='qux')

        assert key1 == key2

    def test_generate_key_different_args(self):
        """Test that different arguments generate different keys."""
        cache = ResponseCache()

        key1 = cache.generate_key(1, 2, 3)
        key2 = cache.generate_key(1, 2, 4)

        assert key1 != key2

    def test_generate_key_kwarg_order_independence(self):
        """Test that kwarg order doesn't affect key."""
        cache = ResponseCache()

        key1 = cache.generate_key(foo='bar', baz='qux')
        key2 = cache.generate_key(baz='qux', foo='bar')

        assert key1 == key2

    def test_set_and_get(self):
        """Test setting and getting values."""
        cache = ResponseCache()

        cache.set('test_key', {'data': 'value'})
        result = cache.get('test_key')

        assert result == {'data': 'value'}
        assert cache.hits == 1
        assert cache.misses == 0

    def test_get_nonexistent(self):
        """Test getting non-existent key returns None."""
        cache = ResponseCache()

        result = cache.get('nonexistent')

        assert result is None
        assert cache.misses == 1

    def test_delete_existing(self):
        """Test deleting existing key."""
        cache = ResponseCache()

        cache.set('test_key', 'value')
        cache.delete('test_key')
        result = cache.get('test_key')

        assert result is None

    def test_delete_nonexistent(self):
        """Test deleting non-existent key doesn't error."""
        cache = ResponseCache()

        # Should not raise exception
        cache.delete('nonexistent')

    def test_clear(self):
        """Test clearing entire cache."""
        cache = ResponseCache()

        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.clear()

        assert cache.get('key1') is None
        assert cache.get('key2') is None

    def test_ttl_expiration(self):
        """Test that cache entries expire after TTL."""
        cache = ResponseCache(maxsize=10, ttl=1)  # 1 second TTL

        cache.set('test_key', 'value')
        assert cache.get('test_key') == 'value'

        # Wait for expiration
        time.sleep(1.5)

        result = cache.get('test_key')
        assert result is None

    def test_maxsize_limit(self):
        """Test that cache respects maxsize limit."""
        cache = ResponseCache(maxsize=2, ttl=60)

        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.set('key3', 'value3')  # Should evict oldest

        # Cache should have at most 2 items
        stats = cache.get_stats()
        assert stats['size'] <= 2

    def test_get_stats(self):
        """Test cache statistics."""
        cache = ResponseCache(maxsize=10, ttl=60)

        cache.set('key1', 'value1')
        cache.get('key1')  # Hit
        cache.get('key2')  # Miss

        stats = cache.get_stats()

        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 50.0
        assert stats['total_requests'] == 2
        assert stats['size'] == 1
        assert stats['maxsize'] == 10
        assert stats['ttl'] == 60


@pytest.mark.unit
class TestCachedDecorator:
    """Test @cached decorator."""

    def test_basic_caching(self):
        """Test that decorator caches function results."""
        call_count = 0

        @cached(ttl=60)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call - should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call - should return cached result
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Function not called again

    def test_different_args_not_cached(self):
        """Test that different arguments create different cache entries."""
        call_count = 0

        @cached(ttl=60)
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        result1 = add(1, 2)
        result2 = add(3, 4)

        assert result1 == 3
        assert result2 == 7
        assert call_count == 2  # Two different calls

    def test_key_prefix(self):
        """Test key_prefix parameter."""
        @cached(key_prefix="test_prefix")
        def simple_func(x):
            return x

        # Should not raise exception
        result = simple_func(42)
        assert result == 42

    def test_condition_function(self):
        """Test conditional caching based on result."""
        call_count = 0

        @cached(condition=lambda result: result > 0)
        def maybe_cache(x):
            nonlocal call_count
            call_count += 1
            return x

        # Positive result - should be cached
        result1 = maybe_cache(5)
        result2 = maybe_cache(5)
        assert result1 == 5
        assert call_count == 1  # Cached

        # Negative result - should NOT be cached
        result3 = maybe_cache(-5)
        result4 = maybe_cache(-5)
        assert result3 == -5
        assert call_count == 3  # Not cached, called twice

    def test_cache_clear_method(self):
        """Test that wrapper has cache_clear method."""
        @cached(ttl=60)
        def func():
            return "value"

        func()
        func.cache_clear()

        # After clear, cache should be empty
        # (We can't directly test this, but verify method exists)
        assert hasattr(func, 'cache_clear')

    def test_cache_stats_method(self):
        """Test that wrapper has cache_stats method."""
        @cached(ttl=60)
        def func():
            return "value"

        func()
        stats = func.cache_stats()

        assert 'hits' in stats
        assert 'misses' in stats
        assert 'total_requests' in stats


@pytest.mark.unit
class TestGlobalCacheFunctions:
    """Test global cache utility functions."""

    def test_get_cache_stats(self):
        """Test global cache stats retrieval."""
        clear_cache()  # Start fresh

        stats = get_cache_stats()

        assert isinstance(stats, dict)
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'size' in stats

    def test_clear_cache(self):
        """Test global cache clearing."""
        # Add some cached data
        @cached(ttl=60)
        def test_func(x):
            return x

        test_func(1)
        test_func(2)

        # Clear cache
        clear_cache()

        # Stats should show empty cache
        stats = get_cache_stats()
        assert stats['size'] == 0

    def test_invalidate_customer_cache(self):
        """Test customer-specific cache invalidation."""
        clear_cache()  # Start fresh

        # Add some cached data
        @cached(ttl=60, key_prefix="customer")
        def get_customer_data(customer_id):
            return f"data_{customer_id}"

        get_customer_data(117)

        # Invalidate
        invalidate_customer_cache(117)

        # Cache should be cleared (current implementation clears all)
        stats = get_cache_stats()
        assert stats['size'] == 0


@pytest.mark.unit
class TestCacheErrorHandling:
    """Test cache error handling."""

    def test_generate_key_error_handling(self):
        """Test that key generation errors are handled gracefully."""
        cache = ResponseCache()

        # Object that can't be serialized to JSON
        class UnserializableObject:
            def __repr__(self):
                raise Exception("Cannot serialize")

        # Should not raise exception, should return error key
        key = cache.generate_key(UnserializableObject())
        assert key.startswith('error_')

    def test_get_error_handling(self):
        """Test that get errors don't crash."""
        cache = ResponseCache()

        # Should handle errors gracefully
        with patch.object(cache.cache, 'get', side_effect=Exception("Error")):
            result = cache.get('test_key')
            assert result is None

    def test_set_error_handling(self):
        """Test that set errors don't crash."""
        cache = ResponseCache()

        # Should handle errors gracefully
        with patch.object(cache.cache, '__setitem__', side_effect=Exception("Error")):
            cache.set('test_key', 'value')  # Should not raise


@pytest.mark.unit
class TestCachePerformance:
    """Test cache performance characteristics."""

    def test_cache_hit_performance(self):
        """Test that cache hits are faster than function execution."""
        import time

        @cached(ttl=60)
        def slow_function(x):
            time.sleep(0.01)  # Simulate slow operation
            return x * 2

        # First call - slow
        start = time.time()
        result1 = slow_function(5)
        first_duration = time.time() - start

        # Second call - fast (cached)
        start = time.time()
        result2 = slow_function(5)
        cached_duration = time.time() - start

        assert result1 == result2 == 10
        assert cached_duration < first_duration / 2  # Cache should be much faster

    def test_cache_stats_tracking(self):
        """Test that cache accurately tracks hits and misses."""
        clear_cache()

        @cached(ttl=60)
        def func(x):
            return x

        # 3 calls with 2 unique arguments
        func(1)  # Miss
        func(1)  # Hit
        func(2)  # Miss
        func(1)  # Hit

        stats = get_cache_stats()
        assert stats['hits'] == 2
        assert stats['misses'] == 2
        assert stats['hit_rate'] == 50.0
