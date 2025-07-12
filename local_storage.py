"""
Local storage module for securely saving user credentials
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)

class LocalCredentialStorage:
    """Handles secure local storage of user credentials"""
    
    def __init__(self):
        logger.info("Initializing LocalCredentialStorage")
        self.app_data_dir = Path.home() / ".emphizor"
        self.credentials_file = self.app_data_dir / "credentials.json"
        self.key_file = self.app_data_dir / "key.key"
        
        # Create app data directory if it doesn't exist
        self.app_data_dir.mkdir(exist_ok=True)
        logger.debug(f"App data directory: {self.app_data_dir}")
        
        # Initialize encryption key
        self._init_encryption_key()
        logger.info("LocalCredentialStorage initialized successfully")
    
    def _init_encryption_key(self):
        """Initialize or load encryption key"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            # Generate new key from machine-specific data
            machine_info = f"{os.getenv('USER', 'default')}-{os.getenv('HOSTNAME', 'default')}-emphizor"
            salt = b'emphizor_salt_2024'  # Fixed salt for consistency
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            self.key = base64.urlsafe_b64encode(kdf.derive(machine_info.encode()))
            
            # Save the key
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
    
    def save_credentials(self, email, password):
        """Save email and encrypted password locally"""
        logger.info(f"Saving credentials for email: {email}")
        try:
            f = Fernet(self.key)
            encrypted_password = f.encrypt(password.encode())
            
            credentials = {
                "email": email,
                "password": base64.urlsafe_b64encode(encrypted_password).decode()
            }
            
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials, f)
            
            logger.info("Credentials saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving credentials: {e}", exc_info=True)
            return False
    
    def load_credentials(self):
        """Load and decrypt saved credentials"""
        logger.info("Loading saved credentials")
        try:
            if not self.credentials_file.exists():
                logger.debug("No credentials file found")
                return None, None
            
            with open(self.credentials_file, 'r') as f:
                credentials = json.load(f)
            
            email = credentials.get("email")
            encrypted_password = base64.urlsafe_b64decode(credentials.get("password").encode())
            
            f = Fernet(self.key)
            password = f.decrypt(encrypted_password).decode()
            
            logger.info(f"Credentials loaded successfully for email: {email}")
            return email, password
        except Exception as e:
            logger.error(f"Error loading credentials: {e}", exc_info=True)
            return None, None
    
    def clear_credentials(self):
        """Clear saved credentials"""
        logger.info("Clearing saved credentials")
        try:
            if self.credentials_file.exists():
                os.remove(self.credentials_file)
                logger.info("Credentials file removed successfully")
            else:
                logger.debug("No credentials file to clear")
            return True
        except Exception as e:
            logger.error(f"Error clearing credentials: {e}", exc_info=True)
            return False
    
    def has_saved_credentials(self):
        """Check if credentials are saved"""
        return self.credentials_file.exists() 