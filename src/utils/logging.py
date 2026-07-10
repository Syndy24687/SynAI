"""
Logging configuration for SynAI.

This module provides centralized logging configuration with Rich console
formatting. It sets up both console and file logging with appropriate
levels and formatters.
"""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler

from src.config.settings import get_settings


def configure_logging() -> None:
    """
    Configure application logging with Rich console output and file logging.

    This function sets up:
    - Root logger with configured level
    - Rich console handler for formatted output
    - File handler for persistent logs

    The logging level is controlled by the APP_LOG_LEVEL environment variable.
    Logs are written to files in the directory specified by LOG_DIR.
    """
    settings = get_settings()

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.app_log_level)

    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_level=True,
        show_path=True,
    )
    console_handler.setLevel(settings.app_log_level)

    formatter = logging.Formatter(
        fmt="%(message)s",
        datefmt="[%X]",
    )
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    log_file = settings.log_dir / "synai.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(settings.app_log_level)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.

    This function provides a consistent way to obtain logger instances
    throughout the application. Loggers are configured to use the
    application's logging setup.

    Args:
        name: The name of the logger, typically the module name.

    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)
