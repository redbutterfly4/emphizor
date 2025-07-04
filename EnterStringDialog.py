from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QLineEdit, 
                              QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, 
                              QPushButton, QMessageBox)
from PySide6.QtCore import Qt

class EnterStringDialog(QDialog):
    def __init__(self, label_message, title, parent, len_limit):
        super().__init__(parent)
        self.setParent(parent)
        self.len_limit = len_limit
        self.setup_ui(label_message, title)
        
    def setup_ui(self, label_message, title):
        self.setWindowTitle(title)
        self.resize(450, 300)
        self.setMinimumSize(300, 200)  # Better minimum for small screens
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply modern styling with purple theme like practice UI
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #667eea, stop: 1 #764ba2);
                color: white;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 16px;
                color: #4c1d95;
                font-weight: 500;
            }
            QLineEdit:focus {
                border-color: rgba(139, 92, 246, 0.8);
                background: white;
                outline: none;
                color: #4c1d95;
            }
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8b5cf6, stop: 1 #7c3aed);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-height: 20px;
                min-width: 80px;
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
                color: white;
                font-weight: 600;
                font-size: 16px;
            }
        """)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)  # Responsive margins
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Input section
        input_layout = QVBoxLayout()
        input_layout.setSpacing(8)
        
        # Label
        self.label = QLabel(label_message)
        self.label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 5px;
            }
        """)
        input_layout.addWidget(self.label)
        
        # Line edit
        self.line_edit = QLineEdit()
        self.line_edit.setMaxLength(self.len_limit)
        self.line_edit.setPlaceholderText(f"Enter text (max {self.len_limit} characters)")
        input_layout.addWidget(self.line_edit)
        
        # Character counter
        self.char_counter = QLabel(f"0/{self.len_limit}")
        self.char_counter.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.char_counter.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                font-style: italic;
                margin-top: 3px;
            }
        """)
        input_layout.addWidget(self.char_counter)
        
        # Connect text changed signal to update counter
        self.line_edit.textChanged.connect(self.update_char_counter)
        
        main_layout.addLayout(input_layout)
        
        # Buttons with responsive layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
                color: white;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        # Add button
        add_btn = QPushButton("Add")
        add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8b5cf6, stop: 1 #7c3aed);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-height: 20px;
                min-width: 80px;
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
        """)
        add_btn.clicked.connect(self.accept_button_pressed)
        button_layout.addWidget(add_btn)
        
        main_layout.addLayout(button_layout)
        
        # Focus on line edit
        self.line_edit.setFocus()
        
    def update_char_counter(self, text):
        """Update the character counter"""
        current_length = len(text)
        self.char_counter.setText(f"{current_length}/{self.len_limit}")
        
        # Change color based on character count
        if current_length >= self.len_limit:
            self.char_counter.setStyleSheet("""
                QLabel {
                    color: #dc2626;
                    font-size: 12px;
                    font-weight: 600;
                    margin-top: 3px;
                }
            """)
        elif current_length >= self.len_limit * 0.9:
            self.char_counter.setStyleSheet("""
                QLabel {
                    color: #fbbf24;
                    font-size: 12px;
                    font-weight: 600;
                    margin-top: 3px;
                }
            """)
        else:
            self.char_counter.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 12px;
                    font-style: italic;
                    margin-top: 3px;
                }
            """)
    
    def is_empty_string_entered(self):
        """Check if the entered string is empty"""
        return self.line_edit.text().strip() == ''
    
    def accept_button_pressed(self):
        """Handle accept button press"""
        if self.is_empty_string_entered():
            QMessageBox.warning(self, "Empty Input", "Please enter some text.")
            return
            
        self.accept() 