from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from datetime import datetime, timezone
from design import Ui_MainWindow
from EnterStringDialog import EnterStringDialog
from AuthDialog import AuthDialog
from ViewCardsDialog import ViewCardsDialog
from PracticeDialog import PracticeDialog
from base_classes import FullCard, App
from fsrs import Card
from ColorProfile import ColorProfile

class MainWindow(QMainWindow):
    tags: set
    tag_buttons: list[QPushButton]
    tag_len_limit = 50
    enter_string_dialog: EnterStringDialog
    color_profile: ColorProfile
    
    def __init__(self):
        super().__init__()
        self.tags = set()  # Initialize the tags attribute as an empty set
        self.tag_buttons = []  # Initialize empty list of buttons
        self.app = None
        self.user = None
        self.color_profile = ColorProfile()
        
        # Show authentication dialog first
        if not self.authenticate_user():
            self.close()
            return
            
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)  # setting ui from Qt Designer
        self.setup_modern_styling()  # Apply modern styling
        self.ui.pushButton.clicked.connect(self.add_tag_clicked)  # connect "Add tag button" with slot
        self.ui.addCartButton.clicked.connect(self.add_card_clicked)  # connect "Add card button" with slot
        self.ui.viewCardsButton.clicked.connect(self.view_cards_clicked)  # connect "View Cards button" with slot
        self.ui.practiceButton.clicked.connect(self.practice_clicked)  # connect "Practice button" with slot
        self.ui.actionSave.triggered.connect(self.save_clicked)  # connect "Save" action with slot
        
        # Update window title with user name
        if self.user:
            self.setWindowTitle(f"Emphizor - {self.user.name}")
            self.update_status_bar()
            # Load existing tags from user's cards
            self.load_existing_tags()
        
        self.connect_buttons_to_update_status_bar()
            
        # Make window responsive with better minimum sizes
        self.resize(1000, 700)
        self.setMinimumSize(600, 400)  # Smaller minimum for better small screen support

        
    def authenticate_user(self):
        """Show authentication dialog and return True if successful"""
        auth_dialog = AuthDialog(self)
        if auth_dialog.exec() == QDialog.DialogCode.Accepted:
            self.app = auth_dialog.get_app()
            self.user = auth_dialog.get_user()
            return True
        return False
        
    def setup_modern_styling(self):
        """Apply modern styling to the application"""
        # Main window styling with purple theme like practice UI
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                color: white;
            }}

            
            QLabel {{
                color: white;
                font-weight: 600;
                font-size: 14px;
            }}
            
            QPushButton {{
                background: rgba(255, 255, 255, 0.95);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 12px 20px;
                font-weight: 700;
                font-size: 14px;
                color: #4c1d95;
                min-height: 20px;
            }}
            
            QPushButton:hover {{
                background: white;
                border-color: rgba(102, 126, 234, 0.5);
                color: #5a67d8;
                transform: translateY(-2px);
            }}
            
            QPushButton:pressed {{
                background: rgba(240, 240, 240, 0.9);
                border-color: #5a67d8;
                color: #4c1d95;
                transform: translateY(0px);
            }}
            
            QPushButton:checked {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #8b5cf6, stop: 1 #7c3aed);
                border-color: #6d28d9;
                color: white;
            }}
            
            QTextEdit {{
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                color: #4c1d95;
                selection-background-color: #8b5cf6;
                selection-color: white;
            }}
            
            QTextEdit:focus {{
                border-color: rgba(139, 92, 246, 0.8);
                background: white;
                color: #4c1d95;
            }}
            
            QMenuBar {{
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                padding: 5px;
            }}
            
            QMenuBar::item {{
                padding: 8px 16px;
                border-radius: 6px;
                background: transparent;
                color: white;
            }}
            
            QMenuBar::item:selected {{
                background: rgba(139, 92, 246, 0.3);
                color: white;
            }}
            
            QMenu {{
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid rgba(139, 92, 246, 0.3);
                border-radius: 12px;
                padding: 8px;
            }}
            
            QMenu::item {{
                padding: 8px 16px;
                border-radius: 6px;
                color: #4c1d95;
            }}
            
            QMenu::item:selected {{
                background: rgba(139, 92, 246, 0.2);
                color: #6d28d9;
            }}
            
            QStatusBar {{
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 5px;
            }}
        """)
        
        # Style specific buttons with purple theme
        if hasattr(self.ui, 'addCartButton'):
            self.ui.addCartButton.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #8b5cf6, stop: 1 #7c3aed);
                    border: 2px solid #6d28d9;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #a78bfa, stop: 1 #8b5cf6);
                    border-color: #8b5cf6;
                    color: white;
                    transform: translateY(-3px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #7c3aed, stop: 1 #6d28d9);
                    color: white;
                    transform: translateY(0px);
                }
            """)
        
        if hasattr(self.ui, 'viewCardsButton'):
            self.ui.viewCardsButton.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #c084fc, stop: 1 #a855f7);
                    border: 2px solid #9333ea;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #ddd6fe, stop: 1 #c084fc);
                    border-color: #c084fc;
                    color: white;
                    transform: translateY(-3px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #a855f7, stop: 1 #9333ea);
                    color: white;
                    transform: translateY(0px);
                }
            """)
        
        if hasattr(self.ui, 'practiceButton'):
            self.ui.practiceButton.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #8b5cf6, stop: 1 #7c3aed);
                    border: 2px solid #6d28d9;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #a78bfa, stop: 1 #8b5cf6);
                    border-color: #8b5cf6;
                    color: white;
                    transform: translateY(-3px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #7c3aed, stop: 1 #6d28d9);
                    color: white;
                    transform: translateY(0px);
                }
            """)
        
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #c084fc, stop: 1 #a855f7);
                    border: 2px solid #9333ea;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #ddd6fe, stop: 1 #c084fc);
                    border-color: #c084fc;
                    color: white;
                    transform: translateY(-3px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #a855f7, stop: 1 #9333ea);
                    color: white;
                    transform: translateY(0px);
                }
            """)
        
    def load_existing_tags(self):
        """Load and display existing tags from user's cards"""
        if not self.user or not self.user.full_cards:
            return
            
        # Extract unique tags from all cards
        all_tags = set()
        for card in self.user.full_cards:
            all_tags.update(card.tags)
        
        # Add tag buttons for each unique tag
        for tag in sorted(all_tags):
            if tag not in self.tags:
                self.tags.add(tag)
                button = QPushButton(self)
                button.setText(tag)
                button.setCheckable(True)
                button.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 255, 255, 0.9);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 12px;
                        padding: 8px 12px;
                        margin: 3px;
                        font-weight: 600;
                        font-size: 13px;
                        color: #4c1d95;
                        min-width: 60px;
                    }
                    QPushButton:hover {
                        background: white;
                        border-color: rgba(139, 92, 246, 0.5);
                        color: #6d28d9;
                    }
                    QPushButton:checked {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #8b5cf6, stop: 1 #7c3aed);
                        border-color: #6d28d9;
                        color: white;
                    }
                """)
                self.ui.verticalLayout.addWidget(button)
                self.tag_buttons.append(button)
                
    def count_due_cards(self):
        """Count how many cards are due for review"""
        if not self.user or not self.user.full_cards:
            return 0
            
        now = datetime.now(timezone.utc)
        due_count = 0
        selected_tags = set()
        for btn in self.tag_buttons:
            if btn.isChecked():
                selected_tags.add(btn.text())
        for full_card in self.user.full_cards:
            if full_card.card.due <= now and full_card.tags <= selected_tags:
                due_count += 1
                
        return due_count
        
    def update_status_bar(self):
        """Update the status bar with current user and card information"""
        if not self.user:
            return
            
        total_cards = len(self.user.full_cards)
        due_cards = self.count_due_cards()
        
        status_text = f"Welcome, {self.user.name} ✨ | {total_cards} cards total | {due_cards} due for review"
        self.statusBar().showMessage(status_text)
        
    def create_enter_string_dialog(self, label_message, title):
        self.enter_string_dialog = EnterStringDialog(label_message, title, self, self.tag_len_limit)
        self.enter_string_dialog.accepted.connect(self.add_tag_button)
        
    def add_tag_button(self):
        tag_text = self.enter_string_dialog.line_edit.text()
        if tag_text not in self.tags:
            self.tags.add(tag_text)
            button = QPushButton(self)
            button.setText(tag_text)
            button.setCheckable(True)  # Make tags selectable
            button.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.9);
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    padding: 8px 12px;
                    margin: 3px;
                    font-weight: 600;
                    font-size: 13px;
                    color: #4c1d95;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background: white;
                    border-color: rgba(139, 92, 246, 0.5);
                    color: #6d28d9;
                }
                QPushButton:checked {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #8b5cf6, stop: 1 #7c3aed)
                    border-color: #6d28d9;
                    color: white;
                }
            """)
            self.ui.verticalLayout.addWidget(button)
            self.tag_buttons.append(button)
            self.tag_buttons[-1].clicked.connect(self.update_status_bar)
            
    def add_tag_clicked(self):
        self.create_enter_string_dialog('Enter tag: ', 'Add tag')
        self.enter_string_dialog.exec()
    def view_cards_clicked(self):
        """Show the view cards dialog"""
        if not self.user:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        view_dialog = ViewCardsDialog(self.user, self)
        view_dialog.exec()
        
    def practice_clicked(self):
        """Start a practice session"""
        if not self.user or not self.app:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        practice_dialog = PracticeDialog(self.user, self.app, self)
        if practice_dialog.cant_practice is False:
            practice_dialog.exec()
        
        # Update status bar after practice session
        self.update_status_bar()
        
    def save_clicked(self):
        """Manual save/sync functionality"""
        if not self.user or not self.app:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        try:
            self.statusBar().showMessage("Saving... 💾", 2000)
            self.app.save_user()
            self.statusBar().showMessage("Data saved successfully! ✅", 3000)
        except Exception as e:
            self.statusBar().showMessage("Save failed! ❌", 3000)
            QMessageBox.warning(self, "Error", f"Failed to save: {str(e)}")
            
    def closeEvent(self, event):
        """Handle application close event - auto-save before closing"""
        if self.user and self.app:
            try:
                self.app.save_user()
                self.statusBar().showMessage("Auto-saved user data before closing", 3000)
            except Exception as e:
                self.statusBar().showMessage("Failed to auto-save! ❌", 3000)
                # Ask user if they want to close without saving
                reply = QMessageBox.question(self, "Save Error", 
                    f"Failed to save data: {str(e)}\n\nDo you want to close without saving?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    event.ignore()
                    return
        
        event.accept()
        
    def add_card_clicked(self):
        """Add a new flashcard"""
        if not self.user or not self.app:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        try:
            # Get question and answer from text fields
            question = self.ui.CardDescriptionTextEdit.toPlainText().strip()
            answer = self.ui.textEdit.toPlainText().strip()
            
            if not question or not answer:
                QMessageBox.warning(self, "Error", "Please enter both question and answer.")
                return
                
            # Get selected tags
            selected_tags = set()
            for button in self.tag_buttons:
                if button.isChecked():
                    selected_tags.add(button.text())
                    
            # Create new card
            card = Card()
            full_card = FullCard(card, question, answer, selected_tags)
            
            # Add to user's cards
            self.user.full_cards.append(full_card)
            
            # Save to database
            self.app.save_user()
            
            # Clear fields
            self.ui.CardDescriptionTextEdit.clear()
            self.ui.textEdit.clear()
            
            # Uncheck all tags
            for button in self.tag_buttons:
                button.setChecked(False)
                
            self.statusBar().showMessage("Card added successfully! 🎉", 3000)
            # Update status bar with new card count after a delay
            self.update_status_bar()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add card: {str(e)}")

    def connect_buttons_to_update_status_bar(self):
        for i in range(len(self.tag_buttons)):
            self.tag_buttons[i].clicked.connect(self.update_status_bar)
def main():
    app = QApplication()
    window = MainWindow()
    if window.user:  # Only show if authentication was successful
        window.show()
        app.exec()

if __name__ == "__main__":
    main()