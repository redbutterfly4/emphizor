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

class MainWindow(QMainWindow):
    tags: list[str]
    tag_buttons: list[QPushButton]
    tag_len_limit = 50
    enter_string_dialog: EnterStringDialog
    
    def __init__(self):
        super().__init__()
        self.tags = []  # Initialize the tags attribute as an empty list
        self.tag_buttons = []  # Initialize empty list of buttons
        self.app = None
        self.user = None
        
        # Show authentication dialog first
        if not self.authenticate_user():
            self.close()
            return
            
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)  # setting ui from Qt Designer
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
        
    def authenticate_user(self):
        """Show authentication dialog and return True if successful"""
        auth_dialog = AuthDialog(self)
        if auth_dialog.exec() == QDialog.DialogCode.Accepted:
            self.app = auth_dialog.get_app()
            self.user = auth_dialog.get_user()
            return True
        return False
        
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
                self.tags.append(tag)
                button = QPushButton(self)
                button.setText(tag)
                button.setCheckable(True)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        padding: 5px;
                        margin: 2px;
                    }
                    QPushButton:checked {
                        background-color: #4CAF50;
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
        
        for full_card in self.user.full_cards:
            if full_card.card.due <= now:
                due_count += 1
                
        return due_count
        
    def update_status_bar(self):
        """Update the status bar with current user and card information"""
        if not self.user:
            return
            
        total_cards = len(self.user.full_cards)
        due_cards = self.count_due_cards()
        
        status_text = f"Logged in as {self.user.name} | {total_cards} cards total | {due_cards} due for review"
        self.statusBar().showMessage(status_text, 10000)
        
    def create_enter_string_dialog(self, label_message, title):
        self.enter_string_dialog = EnterStringDialog(label_message, title, self, self.tag_len_limit)
        self.enter_string_dialog.accepted.connect(self.add_tag_button)
        
    def add_tag_button(self):
        tag_text = self.enter_string_dialog.line_edit.text()
        if tag_text not in self.tags:
            self.tags.append(tag_text)
            button = QPushButton(self)
            button.setText(tag_text)
            button.setCheckable(True)  # Make tags selectable
            button.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                    margin: 2px;
                }
                QPushButton:checked {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
            self.ui.verticalLayout.addWidget(button)
            self.tag_buttons.append(button)
            
    def add_tag_clicked(self):
        self.create_enter_string_dialog('Enter tag: ', 'Add tag')
        
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
        practice_dialog.exec()
        
        # Update status bar after practice session
        self.update_status_bar()
        
    def save_clicked(self):
        """Manual save/sync functionality"""
        if not self.user or not self.app:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        try:
            self.statusBar().showMessage("Saving...", 2000)
            self.app.save_user()
            self.statusBar().showMessage("Data saved successfully!", 3000)
        except Exception as e:
            self.statusBar().showMessage("Save failed!", 3000)
            QMessageBox.warning(self, "Error", f"Failed to save: {str(e)}")
            
    def closeEvent(self, event):
        """Handle application close event - auto-save before closing"""
        if self.user and self.app:
            try:
                self.app.save_user()
                print("Auto-saved user data before closing")
            except Exception as e:
                print(f"Failed to auto-save: {str(e)}")
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
            selected_tags = []
            for button in self.tag_buttons:
                if button.isChecked():
                    selected_tags.append(button.text())
                    
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
                
            self.statusBar().showMessage("Card added and saved successfully!", 3000)
            # Update status bar with new card count after a delay
            self.update_status_bar()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add card: {str(e)}")

def main():
    app = QApplication()
    window = MainWindow()
    if window.user:  # Only show if authentication was successful
        window.show()
        app.exec()

if __name__ == "__main__":
    main()