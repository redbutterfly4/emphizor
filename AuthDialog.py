from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QTabWidget, QWidget, 
                              QMessageBox, QApplication, QCheckBox)
from PySide6.QtCore import Qt
from base_classes import App
from local_storage import LocalCredentialStorage
from ColorProfile import ColorProfile
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Initializing AuthDialog")
        self.app = App()
        self.user = None
        self.credential_storage = LocalCredentialStorage()
        # Get color profile from parent if available, otherwise create default
        self.color_profile = getattr(parent, 'color_profile', ColorProfile())
        logger.debug("AuthDialog base attributes initialized")
        self.setup_ui()
        self.load_saved_credentials()
        logger.info("AuthDialog initialization complete")
        
    def setup_ui(self):
        self.setWindowTitle("Welcome to Emphizor")
        self.resize(800, 800)
        self.setMinimumSize(400, 300)  # Better minimum for small screens
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply modern styling with purple theme like practice UI
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                color: white;
            }}
            QTabWidget::pane {{
                background: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 20px;
                padding: 20px;
            }}
            QTabBar::tab {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-bottom: none;
                border-radius: 15px 15px 0px 0px;
                padding: 15px 25px;
                margin-right: 5px;
                font-weight: 700;
                font-size: 16px;
                color: white;
                min-width: 80px;
            }}
            QTabBar::tab:hover {{
                background: {self.color_profile.gradient_end_color.darker(130).name()};
                border-color: {self.color_profile.gradient_end_color.darker(120).name()};
                color: white;
            }}
            QTabBar::tab:selected {{
                background: rgba(255, 255, 255, 0.95);
                border-color: {self.color_profile.gradient_end_color.lighter(105).name()};
                color: {self.color_profile.gradient_end_color.darker(120).name()};
            }}
            
            QLineEdit {{
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid {self.parent().color_profile.gradient_end_color.darker(115).name()};
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 16px;
                color: {self.parent().color_profile.gradient_end_color.darker(120).name()};
                font-weight: 500;
            }}
            QLineEdit:focus {{
                border-color: {self.parent().color_profile.gradient_end_color.name()};
                background: white;
                outline: none;
                color: {self.parent().color_profile.gradient_end_color.darker(115).name()};
            }}
            QLineEdit::placeholder {{
                color: #9ca3af;
                font-style: italic;
            }}
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(110).name()});
                border: none;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 18px 30px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(110).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(120).name()});
                transform: translateY(-2px);
                color: white;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.lighter(110).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.darker(110).name()});
                transform: translateY(0px);
                color: white;
            }}
            QLabel {{
                color: {self.parent().color_profile.gradient_end_color.darker(110).name()};
                font-weight: 600;
                font-size: 14px;
                margin-bottom: 5px;
            }}
        """)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title and welcome message
        title_label = QLabel("Welcome to Emphizor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Your intelligent flashcard companion")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 20px;
            }}
        """)
        main_layout.addWidget(subtitle_label)
        
        # Tab widget for Sign In / Sign Up
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::tab-bar {{
                alignment: center;
            }}
        """)
        
        # Sign In Tab
        signin_tab = QWidget()
        signin_layout = QVBoxLayout(signin_tab)
        signin_layout.setSpacing(15)
        signin_layout.setContentsMargins(20, 20, 20, 20)
        
        # Email field
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(f"color: {self.parent().color_profile.gradient_end_color.darker(110).name()}; font-weight: 600;")
        signin_layout.addWidget(email_label)
        self.signin_email = QLineEdit()
        self.signin_email.setPlaceholderText("Enter your email address")
        signin_layout.addWidget(self.signin_email)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet(f"color: {self.parent().color_profile.gradient_end_color.darker(110).name()}; font-weight: 600;")
        signin_layout.addWidget(password_label)
        self.signin_password = QLineEdit()
        self.signin_password.setPlaceholderText("Enter your password")
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        signin_layout.addWidget(self.signin_password)
        
        # Remember me checkbox and clear button layout
        remember_layout = QHBoxLayout()
        self.remember_signin = QCheckBox("Remember me")
        self.remember_signin.setStyleSheet(f"""
            QCheckBox {{
                color: {self.parent().color_profile.gradient_end_color.darker(110).name()};
                font-weight: 500;
                margin-top: 10px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {self.parent().color_profile.gradient_end_color.darker(105).name()};
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: {self.parent().color_profile.gradient_end_color.lighter(110).name()};
                border-color: {self.parent().color_profile.gradient_end_color.lighter(110).name()};
            }}
        """)
        remember_layout.addWidget(self.remember_signin)
        
        # Clear saved credentials button
        clear_btn = QPushButton("Clear Saved")
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid  {self.parent().color_profile.gradient_end_color.darker(130).name()};
                border-radius: 8px;
                color:  {self.parent().color_profile.gradient_end_color.darker(120).name()};
                font-size: 12px;
                padding: 5px 10px;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background: {self.parent().color_profile.gradient_end_color.darker(150).name()};
                border-color: {self.parent().color_profile.gradient_end_color.darker(110).name()};
            }}
        """)
        clear_btn.clicked.connect(self.clear_saved_credentials)
        remember_layout.addWidget(clear_btn)
        remember_layout.addStretch()  # Push the button to the left
        
        signin_layout.addLayout(remember_layout)
        
        # Sign in button
        signin_btn = QPushButton("Sign In")
        signin_btn.setStyleSheet(f"""
            QPushButton {{
                 background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(110).name()});
                margin-top: 10px;
                color: white;
            }}
            QPushButton:hover {{
                 background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(110).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(115).name()});
                color: white;
            }}
        """)
        signin_btn.clicked.connect(self.sign_in)
        signin_layout.addWidget(signin_btn)
        
        tab_widget.addTab(signin_tab, "Sign In")
        
        # Sign Up Tab
        signup_tab = QWidget()
        signup_layout = QVBoxLayout(signup_tab)
        signup_layout.setSpacing(15)
        signup_layout.setContentsMargins(20, 20, 20, 20)
        
        # Name field
        name_label = QLabel("Full Name")
        name_label.setStyleSheet(f"color: {self.parent().color_profile.gradient_end_color.darker(110).name()}; font-weight: 600;")
        signup_layout.addWidget(name_label)
        self.signup_name = QLineEdit()
        self.signup_name.setPlaceholderText("Enter your full name")
        signup_layout.addWidget(self.signup_name)
        
        # Email field
        email_label2 = QLabel("Email Address")
        email_label2.setStyleSheet(f"color: {self.parent().color_profile.gradient_end_color.darker(110).name()}; font-weight: 600;")
        signup_layout.addWidget(email_label2)
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email address")
        signup_layout.addWidget(self.signup_email)
        
        # Password field
        password_label2 = QLabel("Password")
        password_label2.setStyleSheet(f"color: {self.parent().color_profile.gradient_end_color.darker(110).name()}; font-weight: 600;")
        signup_layout.addWidget(password_label2)
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Create a secure password")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        signup_layout.addWidget(self.signup_password)
        
        # Remember me checkbox
        self.remember_signup = QCheckBox("Remember me")
        self.remember_signup.setStyleSheet(f"""
            QCheckBox {{
                color: {self.parent().color_profile.gradient_end_color.darker(125).name()};;
                font-weight: 500;
                margin-top: 10px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {self.parent().color_profile.gradient_end_color.lighter(105).name()};;
                border-radius: 4px;
                background: white;
            }}
            QCheckBox::indicator:checked {{
                background: {self.parent().color_profile.gradient_end_color.darker(110).name()};;
                border-color: {self.parent().color_profile.gradient_end_color.darker(110).name()};;
            }}
        """)
        signup_layout.addWidget(self.remember_signup)
        
        # Sign up button
        signup_btn = QPushButton("Create Account")
        signup_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(125).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(125).name()});
                margin-top: 10px;
                color: white;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.lighter(1).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.darker(110).name()});
                color: white;
            }}
        """)
        signup_btn.clicked.connect(self.sign_up)
        signup_layout.addWidget(signup_btn)
        
        tab_widget.addTab(signup_tab, "Sign Up")
        
        main_layout.addWidget(tab_widget)
        
        # Cancel button
        cancel_btn = QPushButton("Exit")
        cancel_btn.setStyleSheet("""
            QPushButton {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 12px 25px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
                color: white;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        main_layout.addWidget(cancel_btn)
        
    def sign_in(self):
        logger.info("Sign in button clicked")
        email = self.signin_email.text().strip()
        password = self.signin_password.text().strip()
        
        if not email or not password:
            logger.warning("Sign in attempted with empty email or password")
            QMessageBox.warning(self, "Missing Information", "Please enter both email and password.")
            return
        
        logger.info(f"Attempting sign in for email: {email}")
        try:
            self.app.login_or_signup(email, password)
            if self.app.user:
                self.user = self.app.user
                logger.info(f"Sign in successful for user: {email}")
                
                # Save credentials if "Remember me" is checked
                if self.remember_signin.isChecked():
                    logger.debug("Saving credentials (remember me checked)")
                    success = self.credential_storage.save_credentials(email, password)
                    if not success:
                        logger.warning("Failed to save credentials locally")
                        QMessageBox.warning(self, "Warning", "Failed to save credentials locally.")
                
                QMessageBox.information(self, "Welcome Back! 🎉", f"Successfully signed in as {self.user.name}")
                self.accept()
            else:
                logger.error("Sign in failed - no user object returned")
                QMessageBox.warning(self, "Sign In Failed", "Please check your credentials and try again.")
        except Exception as e:
            logger.error(f"Sign in failed for {email}: {str(e)}", exc_info=True)
            QMessageBox.warning(self, "Sign In Error", f"Sign in failed: {str(e)}")
            
    def sign_up(self):
        logger.info("Sign up button clicked")
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text().strip()
        
        if not name or not email or not password:
            logger.warning("Sign up attempted with missing information")
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return
        
        logger.info(f"Attempting sign up for email: {email}, name: {name}")
        try:
            self.app.login_or_signup(email, password, name)
            if self.app.user:
                self.user = self.app.user
                logger.info(f"Sign up successful for user: {email}")
                
                # Save credentials if "Remember me" is checked
                if self.remember_signup.isChecked():
                    logger.debug("Saving credentials (remember me checked)")
                    success = self.credential_storage.save_credentials(email, password)
                    if not success:
                        logger.warning("Failed to save credentials locally")
                        QMessageBox.warning(self, "Warning", "Failed to save credentials locally.")
                
                QMessageBox.information(self, "Account Created! 🎉", f"Welcome to Emphizor, {self.user.name}!")
                self.accept()
            else:
                logger.error("Sign up failed - no user object returned")
                QMessageBox.warning(self, "Sign Up Failed", "Account creation failed. Please try again.")
        except Exception as e:
            logger.error(f"Sign up failed for {email}: {str(e)}", exc_info=True)
            QMessageBox.warning(self, "Sign Up Error", f"Sign up failed: {str(e)}")
    
    def load_saved_credentials(self):
        """Load saved credentials and populate the sign-in form"""
        logger.info("Loading saved credentials")
        try:
            email, password = self.credential_storage.load_credentials()
            if email and password:
                logger.info(f"Loaded saved credentials for email: {email}")
                self.signin_email.setText(email)
                self.signin_password.setText(password)
                self.remember_signin.setChecked(True)
            else:
                logger.debug("No saved credentials found")
        except Exception as e:
            logger.error(f"Error loading saved credentials: {e}", exc_info=True)
    
    def clear_saved_credentials(self):
        """Clear saved credentials"""
        try:
            self.credential_storage.clear_credentials()
            self.signin_email.clear()
            self.signin_password.clear()
            self.remember_signin.setChecked(False)
            QMessageBox.information(self, "Cleared", "Saved credentials have been cleared.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to clear credentials: {str(e)}")
            
    def get_app(self):
        return self.app
        
    def get_user(self):
        return self.user 