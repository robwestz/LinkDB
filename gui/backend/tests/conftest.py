"""
Pytest configuration and fixtures for LinkDB tests.

Provides reusable fixtures for testing:
- Test database with sample data
- FastAPI test client
- Mock configurations
- Sample data generators
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import os
import sys

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session")
def test_db_path():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    yield db_path

    # Cleanup
    try:
        os.unlink(db_path)
    except:
        pass


@pytest.fixture(scope="function")
def test_db(test_db_path):
    """
    Create and populate a test database with sample data.

    Returns a connection to the database.
    """
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_history (
            customer_id INTEGER,
            canonical_root TEXT,
            brand TEXT,
            pub_domain TEXT,
            target_url TEXT,
            anchor_text TEXT,
            published_at TEXT
        )
    """)

    # Insert sample data
    sample_data = [
        (1, 'example.com', 'Example Brand', 'blog.publisher1.com', 'https://example.com/page1', 'best seo services', '2024-01-15'),
        (1, 'example.com', 'Example Brand', 'news.publisher2.com', 'https://example.com/page2', 'professional seo', '2024-01-20'),
        (1, 'example.com', 'Example Brand', 'site.publisher3.com', 'https://example.com/', 'click here', '2024-02-10'),
        (2, 'test.com', 'Test Brand', 'blog.publisher1.com', 'https://test.com/about', 'learn more', '2024-01-25'),
        (2, 'test.com', 'Test Brand', 'news.publisher4.com', 'https://test.com/services', 'test services', '2024-02-15'),
    ]

    cursor.executemany("""
        INSERT INTO customer_history
        (customer_id, canonical_root, brand, pub_domain, target_url, anchor_text, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()

    yield conn

    # Cleanup
    conn.close()


@pytest.fixture(scope="function")
def mock_config(test_db_path, monkeypatch):
    """Mock configuration for testing."""
    # Mock environment variables
    test_env = {
        'DATABASE_URL': f'sqlite:///{test_db_path}',
        'SECRET_KEY': 'test-secret-key-12345',
        'ENVIRONMENT': 'testing',
        'DEBUG': 'true',
        'ALLOWED_ORIGINS': '["http://localhost:3000","http://localhost:5173"]',  # JSON format for list
        'CACHE_TTL_SECONDS': '60',
        'CACHE_MAX_SIZE': '100',
        'LOG_LEVEL': 'DEBUG',
    }

    for key, value in test_env.items():
        monkeypatch.setenv(key, value)

    # Import config after setting env vars
    import importlib
    if 'config' in sys.modules:
        importlib.reload(sys.modules['config'])

    from config import settings
    return settings


@pytest.fixture(scope="function")
def test_client(mock_config, test_db):
    """
    Create a FastAPI test client.

    Uses the optimized app with test database.
    """
    # Mock the database path
    with patch('config.get_database_path') as mock_db_path:
        mock_db_path.return_value = Path(test_db.execute("PRAGMA database_list").fetchone()[2])

        # Import app after mocking
        from app_optimized import app

        client = TestClient(app)
        yield client


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return {
        'customer_id': 1,
        'canonical_root': 'example.com',
        'brand': 'Example Brand',
        'total_links': 3,
        'health_score': 75.5
    }


@pytest.fixture
def sample_link_data():
    """Sample link data for testing."""
    return {
        'customer_id': 1,
        'canonical_root': 'example.com',
        'brand': 'Example Brand',
        'pub_domain': 'publisher.com',
        'target_url': 'https://example.com/page',
        'anchor_text': 'test anchor',
        'published_at': '2024-03-15'
    }


@pytest.fixture
def sample_pagination_params():
    """Sample pagination parameters."""
    return {
        'page': 1,
        'page_size': 50
    }


# Performance testing fixture
@pytest.fixture
def benchmark_db(test_db_path):
    """
    Create a larger database for performance testing.

    Generates 1000 links across 10 customers.
    """
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_history (
            customer_id INTEGER,
            canonical_root TEXT,
            brand TEXT,
            pub_domain TEXT,
            target_url TEXT,
            anchor_text TEXT,
            published_at TEXT
        )
    """)

    # Generate 1000 sample records
    import random
    from datetime import datetime, timedelta

    records = []
    base_date = datetime(2024, 1, 1)

    for i in range(1000):
        customer_id = (i % 10) + 1
        pub_date = base_date + timedelta(days=random.randint(0, 90))

        records.append((
            customer_id,
            f'customer{customer_id}.com',
            f'Customer {customer_id} Brand',
            f'publisher{random.randint(1, 50)}.com',
            f'https://customer{customer_id}.com/page{random.randint(1, 100)}',
            f'anchor text {random.randint(1, 50)}',
            pub_date.strftime('%Y-%m-%d')
        ))

    cursor.executemany("""
        INSERT INTO customer_history
        (customer_id, canonical_root, brand, pub_domain, target_url, anchor_text, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()

    yield conn

    conn.close()


# Mock external services
@pytest.fixture
def mock_email_service(monkeypatch):
    """Mock email service for testing scheduled reports."""
    mock_smtp = MagicMock()
    monkeypatch.setattr('smtplib.SMTP', lambda *args, **kwargs: mock_smtp)
    return mock_smtp


@pytest.fixture
def mock_analyzer():
    """Mock analyzer for testing analysis endpoints."""
    mock = MagicMock()
    mock.analyze_customer.return_value = MagicMock(
        canonical_root='example.com',
        brand='Example Brand',
        total_links=100,
        quality_score=85.5,
        diversity_score=78.2
    )
    return mock


# Parametrized fixtures for testing various scenarios
@pytest.fixture(params=[
    {'page': 1, 'page_size': 10},
    {'page': 1, 'page_size': 50},
    {'page': 2, 'page_size': 25},
])
def pagination_scenarios(request):
    """Various pagination scenarios for testing."""
    return request.param


@pytest.fixture(params=[
    '2024-01',
    '2024-02',
    '2024-03',
])
def date_range_scenarios(request):
    """Various date range scenarios for testing."""
    return request.param
