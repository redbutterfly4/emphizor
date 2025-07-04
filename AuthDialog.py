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
        self.setWindowTitle("Emphizor - Authentication")
        self.setFixedSize(400, 300)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Tab widget for Sign In / Sign Up
        tab_widget = QTabWidget()
        
        # Sign In Tab
        signin_tab = QWidget()
        signin_layout = QVBoxLayout(signin_tab)
        
        signin_layout.addWidget(QLabel("Email:"))
        self.signin_email = QLineEdit()
        self.signin_email.setPlaceholderText("Enter your email")
        signin_layout.addWidget(self.signin_email)
        
        signin_layout.addWidget(QLabel("Password:"))
        self.signin_password = QLineEdit()
        self.signin_password.setPlaceholderText("Enter your password")
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        signin_layout.addWidget(self.signin_password)
        
        signin_btn = QPushButton("Sign In")
        signin_btn.clicked.connect(self.sign_in)
        signin_layout.addWidget(signin_btn)
        
        tab_widget.addTab(signin_tab, "Sign In")
        
        # Sign Up Tab
        signup_tab = QWidget()
        signup_layout = QVBoxLayout(signup_tab)
        
        signup_layout.addWidget(QLabel("Name:"))
        self.signup_name = QLineEdit()
        self.signup_name.setPlaceholderText("Enter your name")
        signup_layout.addWidget(self.signup_name)
        
        signup_layout.addWidget(QLabel("Email:"))
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email")
        signup_layout.addWidget(self.signup_email)
        
        signup_layout.addWidget(QLabel("Password:"))
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Enter your password")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        signup_layout.addWidget(self.signup_password)
        
        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.sign_up)
        signup_layout.addWidget(signup_btn)
        
        tab_widget.addTab(signup_tab, "Sign Up")
        
        main_layout.addWidget(tab_widget)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        main_layout.addWidget(cancel_btn)
        
    def sign_in(self):
        email = self.signin_email.text().strip()
        password = self.signin_password.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter both email and password.")
            return
            
        try:
            self.app.login_or_signup(email, password)
            if self.app.user:
                self.user = self.app.user
                QMessageBox.information(self, "Success", f"Successfully signed in as {self.user.name}")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Sign in failed. Please check your credentials.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Sign in failed: {str(e)}")
            
    def sign_up(self):
        name = self.signup_name.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text().strip()
        
        if not name or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
            
        try:
            self.app.login_or_signup(email, password, name)
            if self.app.user:
                self.user = self.app.user
                QMessageBox.information(self, "Success", f"Successfully signed up as {self.user.name}")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Sign up failed. Please try again.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Sign up failed: {str(e)}")
            
    def get_app(self):
        return self.app
        
    def get_user(self):
        return self.user 