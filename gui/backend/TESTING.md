# Testing Guide for LinkDB Backend

This document describes the comprehensive testing infrastructure for the LinkDB backend API.

## Overview

The testing infrastructure includes:
- **117 unit tests** for core modules
- **Integration tests** for API endpoints
- **Performance tests** for critical paths
- **Security tests** for validation and SQL injection prevention
- **Coverage tracking** with >80% target

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_config.py           # Configuration module tests
├── test_validators.py       # Input validation tests
├── test_cache.py            # Response caching tests
├── test_database.py         # Connection pooling tests
├── test_pagination.py       # Pagination utility tests
├── test_api_customers.py    # Customer API endpoints
├── test_api_dashboard.py    # Dashboard API endpoints
└── test_api_links.py        # Links API endpoints
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test Markers

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Security tests
pytest -m security

# Performance tests
pytest -m performance
```

### Run Specific Test Files

```bash
# Test configuration
pytest tests/test_config.py

# Test validators
pytest tests/test_validators.py

# Test API endpoints
pytest tests/test_api_customers.py
```

### Run with Coverage

```bash
# Generate coverage report
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Fixtures

### Database Fixtures

#### `test_db_path`
- **Scope**: Session
- **Purpose**: Creates a temporary SQLite database file
- **Usage**: Used by other fixtures that need a database path

#### `test_db`
- **Scope**: Function
- **Purpose**: Creates and populates test database with sample data
- **Returns**: SQLite connection object
- **Sample Data**:
  - 2 customers (IDs: 1, 2)
  - 5 links across different publishers
  - Date range: 2024-01 to 2024-06

#### `benchmark_db`
- **Scope**: Function
- **Purpose**: Large dataset for performance testing
- **Sample Data**: 1000 links across 10 customers

### Configuration Fixtures

#### `mock_config`
- **Scope**: Function
- **Purpose**: Mocked configuration for testing environment
- **Environment**: Sets test environment variables
- **Usage**: Automatically used by test_client

### API Testing Fixtures

#### `test_client`
- **Scope**: Function
- **Purpose**: FastAPI TestClient for API testing
- **Returns**: Configured TestClient instance
- **Usage**: Use to make requests to API endpoints

```python
def test_api_endpoint(test_client):
    response = test_client.get("/api/v1/customers")
    assert response.status_code == 200
```

### Sample Data Fixtures

#### `sample_customer_data`
Returns dictionary with sample customer data

#### `sample_link_data`
Returns dictionary with sample link data

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

Test individual modules and functions in isolation.

**Modules Tested:**
- `config.py` - Configuration management
- `validators.py` - Input validation
- `cache.py` - Response caching
- `database.py` - Connection pooling
- `pagination.py` - Pagination utilities

**Example:**
```python
@pytest.mark.unit
def test_customer_id_validation():
    """Test that negative customer IDs are rejected."""
    with pytest.raises(ValidationError):
        CustomerQuery(customer_id=-1)
```

### Integration Tests (`@pytest.mark.integration`)

Test API endpoints with real database operations.

**Endpoints Tested:**
- `/api/v1/customers` - Customer list
- `/api/v1/customers/{id}/links` - Customer links
- `/api/v1/customers/{id}/stats` - Customer statistics
- `/api/v1/dashboard/metrics` - Dashboard metrics
- `/api/v1/links` - Links list and filtering

**Example:**
```python
@pytest.mark.integration
def test_get_customers(test_client):
    """Test retrieving customer list."""
    response = test_client.get("/api/v1/customers")
    assert response.status_code == 200
    assert 'items' in response.json()
```

### Security Tests (`@pytest.mark.security`)

Test security validations and SQL injection prevention.

**Tests Include:**
- SQL injection prevention
- Input sanitization
- XSS prevention
- Dangerous pattern detection

**Example:**
```python
@pytest.mark.security
def test_sql_injection_prevention():
    """Test that SQL injection attempts are rejected."""
    with pytest.raises(ValidationError):
        SearchQuery(search_term="'; DROP TABLE customer_history; --")
```

### Performance Tests (`@pytest.mark.performance`)

Test response times and performance characteristics.

**Tests Include:**
- Cache hit performance
- Connection pool performance
- Query optimization
- Pagination performance

**Example:**
```python
@pytest.mark.performance
def test_cache_hit_performance():
    """Test that cache hits are faster than function execution."""
    # First call - slow
    result1 = slow_function(5)
    # Second call - fast (cached)
    result2 = slow_function(5)
    assert cached_duration < first_duration / 2
```

## Test Data

### Sample Customer Data

```python
{
    'customer_id': 1,
    'canonical_root': 'example.com',
    'brand': 'Example Brand',
    'total_links': 3
}
```

### Sample Link Data

```python
{
    'id': 1,
    'customer_id': 1,
    'canonical_root': 'example.com',
    'brand': 'Example Brand',
    'pub_domain': 'blog.pub.com',
    'target_url': 'https://example.com/page1',
    'anchor_text': 'SEO services for businesses',
    'published_at': '2024-01-15',
    'inserted_at': '2024-01-15T10:30:00'
}
```

## Coverage Requirements

The test suite requires **>80% code coverage** to pass.

### Generating Coverage Reports

```bash
# Terminal report with missing lines
pytest --cov=. --cov-report=term-missing

# HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=. --cov-report=xml
```

### Coverage Configuration

Coverage settings are defined in `pytest.ini`:

```ini
[coverage:run]
source = .
omit =
    */tests/*
    */migrations/*
    */__pycache__/*
    */venv/*

[coverage:report]
precision = 2
show_missing = True
fail_under = 80
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Writing New Tests

### Test File Template

```python
"""
Description of what this test file covers.

Tests:
- Feature 1
- Feature 2
- Error handling
"""

import pytest
from module import function_to_test


@pytest.mark.unit
class TestFeatureName:
    """Test feature functionality."""

    def test_basic_functionality(self):
        """Test basic case."""
        result = function_to_test(input_data)
        assert result == expected_output

    def test_edge_case(self):
        """Test edge case."""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Best Practices

1. **One assertion per test** (when possible)
2. **Descriptive test names** that explain what is being tested
3. **Use fixtures** for shared setup/teardown
4. **Test edge cases** and error conditions
5. **Use markers** to categorize tests
6. **Keep tests independent** - no test should depend on another
7. **Use parametrize** for testing multiple inputs

### Example: Parametrized Test

```python
@pytest.mark.parametrize("customer_id,expected", [
    (1, True),
    (0, False),
    (-1, False),
    (1000000, True),
    (9999999, False),
])
def test_customer_id_validation(customer_id, expected):
    """Test various customer IDs."""
    if expected:
        query = CustomerQuery(customer_id=customer_id)
        assert query.customer_id == customer_id
    else:
        with pytest.raises(ValidationError):
            CustomerQuery(customer_id=customer_id)
```

## Troubleshooting

### Common Issues

#### Tests fail with "no such table: customer_history"

**Solution**: Use the `test_db` fixture instead of `test_db_path`

```python
# Wrong
def test_query(test_db_path):
    conn = sqlite3.connect(test_db_path)

# Correct
def test_query(test_db):
    cursor = test_db.cursor()
```

#### Import errors

**Solution**: Ensure `backend` directory is in Python path

```python
# conftest.py
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
```

#### Tests pass individually but fail together

**Solution**: Tests may have shared state. Use function-scoped fixtures or call `clear_cache()` in setup.

#### Coverage too low

**Solution**: Add tests for untested modules. Check coverage report to find missing lines:

```bash
pytest --cov=. --cov-report=term-missing | grep MISS
```

## Test Metrics

Current test coverage:
- **Unit Tests**: 108 tests
- **Integration Tests**: 9 tests
- **Total Tests**: 117 tests
- **Coverage**: >80% (target)

### Test Execution Time

- **Unit tests**: ~2 seconds
- **Integration tests**: ~3 seconds
- **All tests**: ~5 seconds

## Maintenance

### Adding New Tests

1. Create test file in `tests/` directory
2. Import necessary fixtures from `conftest.py`
3. Add appropriate markers (`@pytest.mark.unit`, etc.)
4. Follow naming convention: `test_*.py`
5. Run tests to ensure they pass
6. Check coverage impact

### Updating Fixtures

1. Modify fixture in `conftest.py`
2. Update fixture docstring
3. Run all tests that use the fixture
4. Update this documentation if needed

### Deprecation Warnings

The codebase uses Pydantic V2 with some V1 syntax that will be deprecated. These warnings are expected and will be addressed in a future update:

- `@validator` → `@field_validator`
- `class Config` → `ConfigDict`
- `regex=` → `pattern=`

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## Support

For questions or issues with the testing infrastructure:

1. Check this documentation
2. Review existing test examples
3. Check pytest output for specific error messages
4. Review the fixtures in `conftest.py`
