"""
Configuration module for Emphizor
Handles environment variables and API configuration
"""

import os
from dotenv import load_dotenv
from logger_config import get_logger

# Load environment variables from .env file
load_dotenv()

# Set up logger for this module
logger = get_logger(__name__)

class Config:
    """Configuration class for application settings"""
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL = "google/gemini-2.5-flash-lite-preview-06-17"
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        logger.info("Validating application configuration")
        if not cls.OPENROUTER_API_KEY:
            logger.error("OPENROUTER_API_KEY not found in environment variables")
            raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please create a .env file with your OpenRouter API key.")
        
        logger.info("Configuration validation successful")
        logger.debug(f"OpenRouter model: {cls.OPENROUTER_MODEL}")
        logger.debug(f"OpenRouter base URL: {cls.OPENROUTER_BASE_URL}")
        return True 