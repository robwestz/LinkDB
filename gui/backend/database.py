"""
Database connection management with connection pooling.

Provides efficient database access through connection pooling,
reducing connection overhead and improving performance.
"""

import sqlite3
from contextlib import contextmanager
from queue import Queue, Empty, Full
import threading
from typing import Optional
import time

from config import get_database_path, settings
from logging_config import logger


class ConnectionPool:
    """
    SQLite connection pool for efficient database access.

    Features:
    - Pre-created connections (reduces connection overhead)
    - Thread-safe connection management
    - Automatic connection recycling
    - Connection health checks
    - Performance monitoring
    """

    def __init__(self, database_path: str, pool_size: int = 10, max_overflow: int = 5):
        """
        Initialize connection pool.

        Args:
            database_path: Path to SQLite database
            pool_size: Number of connections to maintain in pool
            max_overflow: Additional connections allowed beyond pool_size
        """
        self.database_path = database_path
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool = Queue(maxsize=pool_size + max_overflow)
        self._lock = threading.Lock()
        self._created_connections = 0
        self._total_connections = 0
        self._checkouts = 0
        self._checkins = 0

        # Pre-create connections
        logger.info(f"Initializing connection pool (size={pool_size}, overflow={max_overflow})")
        self._initialize_pool()

    def _initialize_pool(self):
        """Create initial pool of connections."""
        for _ in range(self.pool_size):
            conn = self._create_connection()
            self.pool.put(conn)

    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection with optimized settings."""
        try:
            conn = sqlite3.connect(
                self.database_path,
                check_same_thread=False,  # Allow connection sharing across threads
                timeout=30.0  # Wait up to 30 seconds for locks
            )

            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")

            # Enable WAL mode for better concurrency
            conn.execute("PRAGMA journal_mode = WAL")

            # Set cache size to 10MB (default is ~2MB)
            conn.execute("PRAGMA cache_size = -10000")

            # Enable memory-mapped I/O (faster reads)
            conn.execute("PRAGMA mmap_size = 268435456")  # 256MB

            # Set synchronous to NORMAL (balance between safety and performance)
            conn.execute("PRAGMA synchronous = NORMAL")

            # Row factory for dict-like access
            conn.row_factory = sqlite3.Row

            with self._lock:
                self._created_connections += 1
                self._total_connections += 1

            logger.debug(f"Created new database connection (total: {self._total_connections})")
            return conn

        except Exception as e:
            logger.error(f"Failed to create database connection: {e}", exc_info=True)
            raise

    def _is_connection_healthy(self, conn: sqlite3.Connection) -> bool:
        """Check if connection is still healthy."""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return True
        except Exception:
            return False

    @contextmanager
    def get_connection(self, timeout: float = 5.0):
        """
        Get a connection from the pool.

        Args:
            timeout: Maximum time to wait for a connection (seconds)

        Yields:
            Database connection

        Example:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        conn = None
        start_time = time.time()

        try:
            # Try to get connection from pool
            try:
                conn = self.pool.get(timeout=timeout)
                self._checkouts += 1
            except Empty:
                # Pool is empty, try to create overflow connection
                with self._lock:
                    if self._total_connections < (self.pool_size + self.max_overflow):
                        conn = self._create_connection()
                        self._checkouts += 1
                    else:
                        # Maximum connections reached
                        wait_time = time.time() - start_time
                        raise Exception(
                            f"Connection pool exhausted. "
                            f"All {self.pool_size + self.max_overflow} connections in use. "
                            f"Waited {wait_time:.2f}s"
                        )

            # Verify connection is healthy
            if not self._is_connection_healthy(conn):
                logger.warning("Unhealthy connection detected, creating new one")
                conn.close()
                with self._lock:
                    self._total_connections -= 1
                conn = self._create_connection()

            # Yield connection to caller
            yield conn

        except Exception as e:
            logger.error(f"Error getting database connection: {e}", exc_info=True)
            raise

        finally:
            # Return connection to pool
            if conn:
                try:
                    # Rollback any uncommitted transactions
                    conn.rollback()

                    # Return to pool if within pool size
                    with self._lock:
                        if self._total_connections <= self.pool_size:
                            try:
                                self.pool.put_nowait(conn)
                                self._checkins += 1
                            except Full:
                                # Pool is full, close overflow connection
                                conn.close()
                                self._total_connections -= 1
                        else:
                            # Overflow connection, close it
                            conn.close()
                            self._total_connections -= 1
                            self._checkins += 1

                except Exception as e:
                    logger.error(f"Error returning connection to pool: {e}", exc_info=True)
                    try:
                        conn.close()
                        with self._lock:
                            self._total_connections -= 1
                    except:
                        pass

    def get_stats(self) -> dict:
        """Get pool statistics."""
        with self._lock:
            return {
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
                "total_connections": self._total_connections,
                "available_connections": self.pool.qsize(),
                "in_use_connections": self._total_connections - self.pool.qsize(),
                "total_checkouts": self._checkouts,
                "total_checkins": self._checkins,
            }

    def close_all(self):
        """Close all connections in the pool."""
        logger.info("Closing all database connections")

        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                conn.close()
                with self._lock:
                    self._total_connections -= 1
            except Empty:
                break
            except Exception as e:
                logger.error(f"Error closing connection: {e}")

        logger.info(f"Closed all connections. Remaining: {self._total_connections}")


# Global connection pool instance
_pool: Optional[ConnectionPool] = None
_pool_lock = threading.Lock()


def get_connection_pool() -> ConnectionPool:
    """Get or create the global connection pool."""
    global _pool

    if _pool is None:
        with _pool_lock:
            if _pool is None:
                db_path = str(get_database_path())
                _pool = ConnectionPool(
                    database_path=db_path,
                    pool_size=10,
                    max_overflow=5
                )
                logger.info(f"✅ Database connection pool initialized: {db_path}")

    return _pool


def get_db_connection():
    """
    Get a database connection from the pool.

    This is a convenience function for backwards compatibility.
    For new code, prefer using the context manager:

        with get_connection_pool().get_connection() as conn:
            # Use conn
    """
    pool = get_connection_pool()
    return pool.get_connection()


# Cleanup on shutdown
import atexit

def cleanup_pool():
    """Close all connections on shutdown."""
    global _pool
    if _pool:
        _pool.close_all()

atexit.register(cleanup_pool)
