#!/usr/bin/env python3
"""
Emphizor - Flashcard Application
Main application entry point with GUI and authentication
"""

import sys
from PySide6.QtWidgets import QApplication
from gui import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Emphizor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Emphizor")
    
    # Create and show main window
    window = MainWindow()
    
    # Only show window if authentication was successful
    if window.user:
        window.show()
        return app.exec()
    else:
        print("Authentication failed or cancelled.")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 