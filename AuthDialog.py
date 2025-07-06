from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QTabWidget, QWidget, 
                              QMessageBox, QApplication)
from PySide6.QtCore import Qt
from base_classes import App

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = App()
        self.user = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Welcome to Emphizor")
        self.resize(800, 800)
        self.setMinimumSize(400, 300)  # Better minimum for small screens
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply modern styling with purple theme like practice UI
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
            }
            QTabWidget::pane {
                background: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 20px;
                padding: 20px;
            }
            QTabBar::tab {
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
            }
            QTabBar::tab:hover {
                background: rgba(139, 92, 246, 0.2);
                border-color: rgba(139, 92, 246, 0.5);
                color: white;
            }
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 0.95);
                border-color: rgba(139, 92, 246, 0.8);
                color: #4c1d95;
            }
            
            QLineEdit {
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid rgba(139, 92, 246, 0.3);
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 16px;
                color: #4c1d95;
                font-weight: 500;
            }
            QLineEdit:focus {
                border-color: #8b5cf6;
                background: white;
                outline: none;
                color: #4c1d95;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
                font-style: italic;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8b5cf6, stop: 1 #7c3aed);
                border: none;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 18px 30px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #a78bfa, stop: 1 #8b5cf6);
                transform: translateY(-2px);
                color: white;
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #7c3aed, stop: 1 #6d28d9);
                transform: translateY(0px);
                color: white;
            }
            QLabel {
                color: #4c1d95;
                font-weight: 600;
                font-size: 14px;
                margin-bottom: 5px;
            }
        """)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title and welcome message
        title_label = QLabel("Welcome to Emphizor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Your intelligent flashcard companion")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(subtitle_label)
        
        # Tab widget for Sign In / Sign Up
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                alignment: center;
            }
        """)
        
        # Sign In Tab
        signin_tab = QWidget()
        signin_layout = QVBoxLayout(signin_tab)
        signin_layout.setSpacing(15)
        signin_layout.setContentsMargins(20, 20, 20, 20)
        
        # Email field
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("color: #4c1d95; font-weight: 600;")
        signin_layout.addWidget(email_label)
        self.signin_email = QLineEdit()
        self.signin_email.setPlaceholderText("Enter your email address")
        signin_layout.addWidget(self.signin_email)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #4c1d95; font-weight: 600;")
        signin_layout.addWidget(password_label)
        self.signin_password = QLineEdit()
        self.signin_password.setPlaceholderText("Enter your password")
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        signin_layout.addWidget(self.signin_password)
        
        # Sign in button
        signin_btn = QPushButton("Sign In")
        signin_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8b5cf6, stop: 1 #7c3aed);
                margin-top: 10px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #a78bfa, stop: 1 #8b5cf6);
                color: white;
            }
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
        name_label.setStyleSheet("color: #4c1d95; font-weight: 600;")
        signup_layout.addWidget(name_label)
        self.signup_name = QLineEdit()
        self.signup_name.setPlaceholderText("Enter your full name")
        signup_layout.addWidget(self.signup_name)
        
        # Email field
        email_label2 = QLabel("Email Address")
        email_label2.setStyleSheet("color: #4c1d95; font-weight: 600;")
        signup_layout.addWidget(email_label2)
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email address")
        signup_layout.addWidget(self.signup_email)
        
        # Password field
        password_label2 = QLabel("Password")
        password_label2.setStyleSheet("color: #4c1d95; font-weight: 600;")
        signup_layout.addWidget(password_label2)
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Create a secure password")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        signup_layout.addWidget(self.signup_password)
        
        # Sign up button
        signup_btn = QPushButton("Create Account")
        signup_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #c084fc, stop: 1 #a855f7);
                margin-top: 10px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ddd6fe, stop: 1 #c084fc);
                color: white;
            }
        """)
        signup_btn.clicked.connect(self.sign_up)
        signup_layout.addWidget(signup_btn)
        
        tab_widget.addTab(signup_tab, "Sign Up")
        
        main_layout.addWidget(tab_widget)
        
        # Cancel button
        cancel_btn = QPushButton("Exit")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 12px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
                color: white;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        main_layout.addWidget(cancel_btn)
        
    def sign_in(self):
        email = self.signin_email.text().strip()
        password = self.signin_password.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Missing Information", "Please enter both email and password.")
            return
            
        try:
            self.app.login_or_signup(email, password)
            if self.app.user:
                self.user = self.app.user
                QMessageBox.information(self, "Welcome Back! 🎉", f"Successfully signed in as {self.user.name}")
                self.accept()
            else:
                QMessageBox.warning(self, "Sign In Failed", "Please check your credentials and try again.")
        except Exception as e:
            QMessageBox.warning(self, "Sign In Error", f"Sign in failed: {str(e)}")
            
    def sign_up(self):
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text().strip()
        
        if not name or not email or not password:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return
            
        try:
            self.app.login_or_signup(email, password, name)
            if self.app.user:
                self.user = self.app.user
                QMessageBox.information(self, "Account Created! 🎉", f"Welcome to Emphizor, {self.user.name}!")
                self.accept()
            else:
                QMessageBox.warning(self, "Sign Up Failed", "Account creation failed. Please try again.")
        except Exception as e:
            QMessageBox.warning(self, "Sign Up Error", f"Sign up failed: {str(e)}")
            
    def get_app(self):
        return self.app
        
    def get_user(self):
        return self.user 