"""
Logging configuration for Emphizor application
Provides centralized logging setup with file rotation and multiple log levels
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name=None, level=logging.INFO):
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Logger name (defaults to module name)
        level: Logging level (default: INFO)
    
    Returns:
        Logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name or __name__)
    
    # Avoid adding multiple handlers to the same logger
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation (keeps last 5 files, max 10MB each)
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / 'emphizor.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name=None):
    """Get a logger instance for the calling module"""
    return setup_logger(name)

# Create application-wide logger
app_logger = setup_logger('emphizor')

# Log application startup
app_logger.info("="*60)
app_logger.info("EMPHIZOR APPLICATION STARTUP")
app_logger.info("="*60) 