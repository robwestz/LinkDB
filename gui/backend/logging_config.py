"""
Structured logging configuration for LinkDB.

Provides JSON-formatted logs with request tracking, performance metrics,
and proper log rotation.
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
import traceback

from config import settings


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.

    Converts log records to JSON format for easier parsing and analysis.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_data["request_id"] = record.request_id

        if hasattr(record, 'customer_id'):
            log_data["customer_id"] = record.customer_id

        if hasattr(record, 'duration_ms'):
            log_data["duration_ms"] = record.duration_ms

        if hasattr(record, 'status_code'):
            log_data["status_code"] = record.status_code

        # Add any other extra attributes
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'pathname', 'process', 'processName', 'relativeCreated',
                          'thread', 'threadName', 'exc_info', 'exc_text', 'stack_info',
                          'getMessage', 'message', 'asctime']:
                if not key.startswith('_'):
                    log_data[key] = value

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info)
            }

        return json.dumps(log_data, default=str)


class HumanReadableFormatter(logging.Formatter):
    """
    Human-readable formatter for console output during development.
    """

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors for console."""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

        # Build message
        message = f"{color}[{record.levelname}]{reset} {timestamp} - {record.name} - {record.getMessage()}"

        # Add request ID if present
        if hasattr(record, 'request_id'):
            message += f" [request_id={record.request_id}]"

        # Add duration if present
        if hasattr(record, 'duration_ms'):
            message += f" [duration={record.duration_ms}ms]"

        # Add exception if present
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"

        return message


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get or create logger
    logger = logging.getLogger("linkdb")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with human-readable format (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.ENVIRONMENT == "development" or settings.DEBUG:
        console_handler.setFormatter(HumanReadableFormatter())
    else:
        console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # File handler with JSON format and rotation
    file_handler = RotatingFileHandler(
        filename=settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    # Log initialization
    logger.info(
        "Logging initialized",
        extra={
            "environment": settings.ENVIRONMENT,
            "log_level": settings.LOG_LEVEL,
            "log_file": settings.LOG_FILE
        }
    )

    return logger


# Global logger instance
logger = setup_logging()


def log_request(request_id: str, method: str, path: str, client: str):
    """Log incoming HTTP request."""
    logger.info(
        f"{method} {path}",
        extra={
            "request_id": request_id,
            "method": method,
            "path": path,
            "client": client,
            "event": "request_started"
        }
    )


def log_response(request_id: str, status_code: int, duration_ms: float):
    """Log HTTP response."""
    logger.info(
        f"Response {status_code}",
        extra={
            "request_id": request_id,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "event": "request_completed"
        }
    )


def log_error(request_id: str, error: Exception, context: Dict[str, Any] = None):
    """Log error with context."""
    extra = {
        "request_id": request_id,
        "error_type": type(error).__name__,
        "event": "error"
    }

    if context:
        extra.update(context)

    logger.error(
        f"Error: {str(error)}",
        extra=extra,
        exc_info=True
    )


def log_database_query(query: str, params: tuple, duration_ms: float, rows_affected: int = None):
    """Log database query for performance monitoring."""
    logger.debug(
        f"Database query executed",
        extra={
            "query": query[:200] + "..." if len(query) > 200 else query,  # Truncate long queries
            "params_count": len(params) if params else 0,
            "duration_ms": round(duration_ms, 2),
            "rows_affected": rows_affected,
            "event": "database_query"
        }
    )


# Export logger for use in other modules
__all__ = ['logger', 'log_request', 'log_response', 'log_error', 'log_database_query']
