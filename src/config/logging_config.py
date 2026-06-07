<<<<<<< HEAD
"""
Logging configuration
"""
import logging
import logging.handlers
from pathlib import Path
from src.config.settings import settings


def setup_logging():
    """Configure logging for the application"""

    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
=======
"""
Logging configuration
"""
import logging
import logging.handlers
from pathlib import Path
from src.config.settings import settings


def setup_logging():
    """Configure logging for the application"""

    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
>>>>>>> 541a7a3cfad060b477d29a46b7de3894e937aa34
