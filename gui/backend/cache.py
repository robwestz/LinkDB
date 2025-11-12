"""
Response caching layer for LinkDB API.

Provides in-memory caching with TTL to reduce database load and improve response times.
"""

import hashlib
import json
import time
from typing import Any, Optional, Callable
from functools import wraps
from cachetools import TTLCache

from config import settings
from logging_config import logger


class ResponseCache:
    """
    In-memory response cache with TTL (Time To Live).

    Features:
    - Automatic expiration based on TTL
    - Size-limited (LRU eviction when full)
    - Cache key generation from function arguments
    - Cache hit/miss tracking
    - Conditional caching based on predicates
    """

    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        """
        Initialize cache.

        Args:
            maxsize: Maximum number of cached items
            ttl: Time to live in seconds (default 5 minutes)
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.hits = 0
        self.misses = 0
        self.ttl = ttl

        logger.info(f"Response cache initialized (maxsize={maxsize}, ttl={ttl}s)")

    def generate_key(self, *args, **kwargs) -> str:
        """
        Generate cache key from arguments.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            MD5 hash of serialized arguments
        """
        try:
            # Create a deterministic string from args and kwargs
            key_data = {
                'args': args,
                'kwargs': {k: v for k, v in sorted(kwargs.items())}
            }

            # Serialize to JSON (sorted keys for consistency)
            key_string = json.dumps(key_data, sort_keys=True, default=str)

            # Generate MD5 hash
            return hashlib.md5(key_string.encode()).hexdigest()

        except Exception as e:
            logger.error(f"Error generating cache key: {e}", exc_info=True)
            # Return a unique key that won't match anything
            return f"error_{time.time()}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.cache.get(key)
            if value is not None:
                self.hits += 1
                logger.debug(f"Cache HIT: {key}")
                return value
            else:
                self.misses += 1
                logger.debug(f"Cache MISS: {key}")
                return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    def set(self, key: str, value: Any):
        """Set value in cache."""
        try:
            self.cache[key] = value
            logger.debug(f"Cache SET: {key}")
        except Exception as e:
            logger.error(f"Error setting cache: {e}")

    def delete(self, key: str):
        """Delete value from cache."""
        try:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Cache DELETE: {key}")
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")

    def clear(self):
        """Clear all cached values."""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "ttl": self.ttl,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests
        }


# Global cache instance
_cache = ResponseCache(
    maxsize=settings.CACHE_MAX_SIZE,
    ttl=settings.CACHE_TTL_SECONDS
)


def cached(
    ttl: Optional[int] = None,
    key_prefix: str = "",
    condition: Optional[Callable] = None
):
    """
    Decorator to cache function responses.

    Args:
        ttl: Time to live in seconds (overrides default)
        key_prefix: Prefix for cache key (useful for namespacing)
        condition: Optional function to determine if response should be cached

    Example:
        @cached(ttl=300, key_prefix="customers")
        def get_customer(customer_id: int):
            # Expensive operation
            return result

    Example with condition:
        @cached(condition=lambda result: result.get('success', False))
        def get_data():
            # Only cache successful responses
            return result
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{_cache.generate_key(*args, **kwargs)}"

            # Try to get from cache
            cached_value = _cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = func(*args, **kwargs)

            # Check condition if provided
            if condition and not condition(result):
                logger.debug(f"Skipping cache for {cache_key} (condition not met)")
                return result

            # Cache the result
            _cache.set(cache_key, result)

            return result

        # Add cache control methods to wrapper
        wrapper.cache_clear = lambda: _cache.clear()
        wrapper.cache_stats = lambda: _cache.get_stats()

        return wrapper

    return decorator


def invalidate_customer_cache(customer_id: int):
    """
    Invalidate all cache entries for a specific customer.

    Useful when customer data is updated.
    """
    # Since we can't easily iterate TTLCache to find matching keys,
    # we clear the entire cache. In production, consider using Redis
    # with pattern-based key deletion.
    _cache.clear()
    logger.info(f"Cache invalidated for customer {customer_id}")


def get_cache_stats() -> dict:
    """Get global cache statistics."""
    return _cache.get_stats()


def clear_cache():
    """Clear the global cache."""
    _cache.clear()


# Export main functions
__all__ = [
    'cached',
    'invalidate_customer_cache',
    'get_cache_stats',
    'clear_cache'
]
