#!/usr/bin/env python3
"""
Emphizor - Flashcard Application
Main application entry point with GUI and authentication
"""

import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)

def main():
    """Main application entry point"""
    logger.info("Starting Emphizor application")
    
    try:
        app = QApplication(sys.argv)
        logger.info("Qt Application created successfully")
        
        # Set application metadata
        app.setApplicationName("Emphizor")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Emphizor")
        logger.info("Application metadata set - Name: Emphizor, Version: 1.0.0")
        
        # Create and show main window
        logger.info("Creating main window...")
        window = MainWindow()
        logger.info("Main window created successfully")
        
        # Only show window if authentication was successful
        if window.user:
            logger.info(f"User authentication successful for: {window.user.email}")
            window.show()
            logger.info("Main window shown, entering application event loop")
            return app.exec()
        else:
            logger.warning("Authentication failed or cancelled by user")
            return 0
            
    except Exception as e:
        logger.error(f"Critical error in main application: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    logger.info("Emphizor application starting up...")
    exit_code = main()
    logger.info(f"Emphizor application exiting with code: {exit_code}")
    sys.exit(exit_code) 