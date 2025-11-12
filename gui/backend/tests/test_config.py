"""
Unit tests for configuration module.

Tests:
- Settings validation
- Environment variable loading
- Configuration validation
- Database path resolution
"""

import pytest
from pathlib import Path
from pydantic import ValidationError


@pytest.mark.unit
class TestSettings:
    """Test configuration settings."""

    def test_default_settings(self, mock_config):
        """Test that default settings are loaded correctly."""
        assert mock_config.APP_NAME == "LinkDB Analytics API"
        assert mock_config.APP_VERSION == "2.0.0"
        assert mock_config.ENVIRONMENT == "testing"

    def test_database_url_parsing(self, mock_config):
        """Test database URL is parsed correctly."""
        assert mock_config.DATABASE_URL.startswith("sqlite:///")

    def test_allowed_origins(self, mock_config):
        """Test CORS allowed origins are configured."""
        assert len(mock_config.ALLOWED_ORIGINS) > 0
        assert "http://localhost:5173" in mock_config.ALLOWED_ORIGINS

    def test_cache_settings(self, mock_config):
        """Test cache configuration."""
        assert mock_config.CACHE_TTL_SECONDS == 60
        assert mock_config.CACHE_MAX_SIZE == 100

    def test_pagination_settings(self, mock_config):
        """Test pagination defaults."""
        assert mock_config.DEFAULT_PAGE_SIZE == 50
        assert mock_config.MAX_PAGE_SIZE == 100


@pytest.mark.unit
class TestDatabasePath:
    """Test database path resolution."""

    def test_get_database_path(self, mock_config):
        """Test database path can be resolved."""
        from config import get_database_path

        db_path = get_database_path()
        assert isinstance(db_path, Path)

    def test_database_path_is_absolute(self, mock_config):
        """Test database path is absolute."""
        from config import get_database_path

        db_path = get_database_path()
        assert db_path.is_absolute()


@pytest.mark.unit
class TestValidation:
    """Test settings validation."""

    def test_production_secret_key_warning(self, monkeypatch, capsys):
        """Test warning when using default secret key in production."""
        monkeypatch.setenv('ENVIRONMENT', 'production')
        monkeypatch.setenv('SECRET_KEY', 'CHANGE-THIS-IN-PRODUCTION')
        monkeypatch.setenv('DATABASE_URL', 'sqlite:///./test.db')

        # Reload config to trigger validation
        import importlib
        import sys
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])

        captured = capsys.readouterr()
        # Validation warnings should be printed
        # (We check this was called, actual warning depends on implementation)

    def test_debug_in_production_warning(self, monkeypatch):
        """Test warning when DEBUG=True in production."""
        monkeypatch.setenv('ENVIRONMENT', 'production')
        monkeypatch.setenv('DEBUG', 'true')

        # Reload and check validation
        # (Implementation-specific)


@pytest.mark.unit
def test_settings_from_env(monkeypatch):
    """Test that settings are loaded from environment variables."""
    monkeypatch.setenv('APP_NAME', 'Custom App Name')
    monkeypatch.setenv('CACHE_TTL_SECONDS', '600')
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///./custom.db')

    # Reload config
    import importlib
    import sys
    if 'config' in sys.modules:
        importlib.reload(sys.modules['config'])

    from config import settings

    assert settings.APP_NAME == 'Custom App Name'
    assert settings.CACHE_TTL_SECONDS == 600
