"""
Configuration module for Emphizor
Handles environment variables and API configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for application settings"""
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_MODEL = "google/gemini-2.5-flash-lite-preview-06-17"
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please create a .env file with your OpenRouter API key.")
        
        return True 