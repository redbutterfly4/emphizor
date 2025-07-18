from PySide6.QtWidgets import QColorDialog, QApplication, QMainWindow, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialogButtonBox, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal
from datetime import datetime, timezone
import requests
import json
from design import Ui_MainWindow
from EnterStringDialog import EnterStringDialog
from AuthDialog import AuthDialog
from ViewCardsDialog import ViewCardsDialog
from PracticeDialog import PracticeDialog
from ConceptConnectDialog import ConceptConnectDialog
from base_classes import FullCard, App
from fsrs import Card
from ColorProfile import ColorProfile
from config import Config
from logger_config import get_logger
from sound_manager import SoundManager

# Set up logger for this module
logger = get_logger(__name__)

class AnswerGenerationWorker(QThread):
    """Worker thread for generating answers using OpenRouter API"""
    answer_generated = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, question):
        super().__init__()
        self.question = question
        logger.debug(f"AnswerGenerationWorker initialized with question: {question[:50]}...")
        
    def run(self):
        logger.info("Starting AI answer generation process")
        try:
            # Validate config
            logger.debug("Validating OpenRouter configuration")
            Config.validate_config()
            logger.debug("OpenRouter configuration validated successfully")
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            
            data = {
                "model": Config.OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert tutor helping create flashcards. Given a question, provide a clear, concise, and accurate answer that would be perfect for a flashcard. Keep it focused and educational. Answer in the language of the question. Include only the answer, no other text or symbols. Use plain text without markdown formatting."
                    },
                    {
                        "role": "user",
                        "content": f"Create a flashcard answer for this question: {self.question}"
                    }
                ],
                "max_tokens": 777,
                "temperature": 0.7
            }
            
            logger.info(f"Sending request to OpenRouter API with model: {Config.OPENROUTER_MODEL}")
            response = requests.post(
                Config.OPENROUTER_BASE_URL,
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            logger.info(f"API response received with status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    answer = result['choices'][0]['message']['content'].strip()
                    logger.info(f"AI answer generated successfully (length: {len(answer)} characters)")
                    self.answer_generated.emit(answer)
                else:
                    logger.error("API response missing choices or empty response")
                    self.error_occurred.emit("No answer generated from API")
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                self.error_occurred.emit(f"API request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error in AI answer generation: {str(e)}", exc_info=True)
            self.error_occurred.emit(f"Error generating answer: {str(e)}")

class MainWindow(QMainWindow):
    tags: set
    tag_buttons: list[QPushButton]
    tag_len_limit = 50
    enter_string_dialog: EnterStringDialog
    color_profile: ColorProfile
    first_color_dialog: QColorDialog
    second_color_dialog: QColorDialog
    def __init__(self):
        super().__init__()
        logger.info("Initializing MainWindow")
        self.tags = set()  # Initialize the tags attribute as an empty set
        self.tag_buttons = []  # Initialize empty list of buttons
        self.app = None
        self.user = None
        self.color_profile = ColorProfile()
        self.sound_manager = SoundManager(self)
        logger.debug("MainWindow base attributes initialized")
        
        # Show authentication dialog first
        logger.info("Starting user authentication process")
        if not self.authenticate_user():
            logger.warning("User authentication failed, closing application")
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
        self.ui.actionfirst_color.triggered.connect(self.first_color_action_clicked)
        self.ui.actionsecond_color.triggered.connect(self.second_color_action_clicked)
        self.ui.delete_tag_button.clicked.connect(self.delete_tag_button_clicked)

        # Add Concept Connect game button
        self.concept_connect_button = QPushButton("🎯 Concept Connect")
        self.concept_connect_button.clicked.connect(self.concept_connect_clicked)
        self.ui.buttonsLayout.addWidget(self.concept_connect_button)
        
        # Add AI generation functionality
        self.answer_worker = None
        self.setup_ai_generation()
        # Update window title with user name
        if self.user:
            self.setWindowTitle(f"Emphizor - {self.user.name}")
            self.update_status_bar()
            # Load existing tags from user's cards
            self.load_existing_tags()
        
        self.connect_buttons_to_update_status_bar()
    def set_generate_button_styling(self):
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
               
                border-radius: 0px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.gradient_end_color.name()}, stop: 1 {self.color_profile.main_color.name()});
                border-color: {self.color_profile.main_color.name()};
                color: white;
                transform: translateY(-3px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.darker(105).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                color: white;
                transform: translateY(0px);
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.5);
            }}
        """)
    def setup_ai_generation(self):
        """Setup AI generation functionality for the answer field"""
        # Add Generate Answer button
        self.generate_btn = QPushButton("Generate Answer")
        self.generate_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                border: 2px solid {self.color_profile.gradient_end_color.darker(105).name()};
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 25px;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.gradient_end_color.name()}, stop: 1 {self.color_profile.main_color.name()});
                border-color: {self.color_profile.main_color.name()};
                color: white;
                transform: translateY(-3px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.darker(105).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                color: white;
                transform: translateY(0px);
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.5);
            }}
        """)
        self.generate_btn.clicked.connect(self.generate_answer)
        
        # Add the button to the layout after the question field
        self.ui.AddCardInterfaceLayout.insertWidget(1, self.generate_btn)
        
    def generate_answer(self):
        """Generate answer using OpenRouter API"""
        question = self.ui.CardDescriptionTextEdit.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please enter a question first.")
            return
        
        # If a worker is already running, don't start another one
        if self.answer_worker and self.answer_worker.isRunning():
            return
        
        # Clean up any previous worker
        if self.answer_worker:
            self.answer_worker.deleteLater()
            self.answer_worker = None
        
        # Disable generate button during generation
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("Generating...")
        
        # Start the worker thread
        self.answer_worker = AnswerGenerationWorker(question)
        self.answer_worker.answer_generated.connect(self.on_answer_generated)
        self.answer_worker.error_occurred.connect(self.on_error_occurred)
        self.answer_worker.finished.connect(self.on_worker_finished)
        self.answer_worker.start()
        
    def on_answer_generated(self, answer):
        """Handle successful answer generation"""
        self.ui.textEdit.setPlainText(answer)
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Answer")
        
    def on_error_occurred(self, error_message):
        """Handle error during answer generation"""
        QMessageBox.warning(self, "Error", f"Failed to generate answer: {error_message}")
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Answer")
        
    def on_worker_finished(self):
        """Handle worker thread completion"""
        if self.answer_worker:
            self.answer_worker.deleteLater()
            self.answer_worker = None
            
        # Make window responsive with better minimum sizes
        self.resize(1000, 700)
        self.setMinimumSize(600, 400)  # Smaller minimum for better small screen support

        
    def authenticate_user(self):
        """Show authentication dialog and return True if successful"""
        logger.info("Showing authentication dialog")
        auth_dialog = AuthDialog(self)
        if auth_dialog.exec() == QDialog.DialogCode.Accepted:
            self.app = auth_dialog.get_app()
            self.user = auth_dialog.get_user()
            logger.info(f"Authentication successful for user: {self.user.email if self.user else 'Unknown'}")
            return True
        logger.warning("Authentication dialog cancelled or failed")
        return False
    
    def get_selected_tags(self):
        res = set()
        for button in self.tag_buttons:
            if button.isChecked() is True:
                res.add(button.text())
        return res

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
                color: {self.color_profile.gradient_end_color.darker(140).name()};
                min-height: 20px;
            }}
            
            QPushButton:hover {{
                background: white;
                border-color: {self.color_profile.gradient_end_color.darker(140).name()};
                color: ;
                transform: translateY(-2px);
            }}
            
            QPushButton:pressed {{
                background: rgba(240, 240, 240, 0.9);
                border-color: {self.color_profile.main_color.lighter(120).name()};
                color: {self.color_profile.main_color.darker(140).name()};
                transform: translateY(0px);
            }}
            
            QPushButton:checked {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                border-color: {self.color_profile.gradient_end_color.darker(110).name()};
                color: white;
            }}
            
            QTextEdit {{
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                color: {self.color_profile.main_color.darker(140).name()};
                selection-background-color: {self.color_profile.gradient_end_color.darker(130).name()};
                selection-color: white;
            }}
            
            QTextEdit:focus {{
                border-color: {self.color_profile.gradient_end_color.darker(105).name()};
                background: white;
                color: {self.color_profile.main_color.darker(140).name()};
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
                color: white;
            }}
            
            QMenuBar::item:selected {{
                background: {self.color_profile.gradient_end_color.darker(130).name()};
                color: white;
            }}
            
            QMenu {{
                background: rgba(255, 255, 255, 0.98);
                border: 2px solid {self.color_profile.gradient_end_color.darker(130).name()};
                border-radius: 12px;
                padding: 8px;
            }}
            
            QMenu::item {{
                padding: 8px 16px;
                border-radius: 6px;
                color: {self.color_profile.main_color.darker(140).name()};
            }}
            
            QMenu::item:selected {{
                background: {self.color_profile.main_color.darker(140).name()}
                color: {self.color_profile.gradient_end_color.darker(110).name()};
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
            self.ui.addCartButton.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                    border: 2px solid {self.color_profile.gradient_end_color.darker(110).name()};
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.darker(110).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(120).name()});
                    border-color: {self.color_profile.gradient_end_color.darker(130).name()};
                    color: white;
                    transform: translateY(-3px);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.lighter(110).name()}, stop: 1 {self.color_profile.gradient_end_color.darker(110).name()});
                    color: white;
                    transform: translateY(0px);
                }}
            """)
        
        if hasattr(self.ui, 'viewCardsButton'):
            self.ui.viewCardsButton.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.lighter(110).name()}, stop: 1 {self.color_profile.gradient_end_color.darker(105).name()});
                    border: 2px solid {self.color_profile.gradient_end_color.name()};
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.lighter(120).name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                    border-color: {self.color_profile.gradient_end_color.lighter(110).name()};
                    color: white;
                    transform: translateY(-3px);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.darker(105).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(105).name()});
                    color: white;
                    transform: translateY(0px);
                }}
            """)
        
        if hasattr(self.ui, 'practiceButton'):
            self.ui.practiceButton.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                    border: 2px solid {self.color_profile.gradient_end_color.darker(110).name()};
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 15px 25px;
                    min-height: 25px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.darker(130).name()});
                    border-color: {self.color_profile.gradient_end_color.darker(130).name()};
                    color: white;
                    transform: translateY(-3px);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.gradient_end_color.lighter(110).name()}, stop: 1 {self.color_profile.gradient_end_color.darker(110).name()});
                    color: white;
                    transform: translateY(0px);
                }}
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
                button.setStyleSheet(f"""
                    QPushButton {{
                        background: rgba(255, 255, 255, 0.9);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 12px;
                        padding: 8px 12px;
                        margin: 3px;
                        font-weight: 600;
                        font-size: 13px;
                        color: {self.color_profile.main_color.darker(140).name()};
                        min-width: 60px;
                    }}
                    QPushButton:hover {{
                        background: white;
                        border-color: {self.color_profile.gradient_end_color.darker(115).name()};
                        color: {self.color_profile.gradient_end_color.darker(110).name()};
                    }}
                    QPushButton:checked {{
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                        border-color: {self.color_profile.gradient_end_color.darker(110).name()};
                        color: white;
                    }}
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
        
    def tag_button_set_styling(self, button):
        button.setStyleSheet(f"""
                    QPushButton {{
                        background: rgba(255, 255, 255, 0.9);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 12px;
                        padding: 8px 12px;
                        margin: 3px;
                        font-weight: 600;
                        font-size: 13px;
                        color: {self.color_profile.main_color.darker(140).name()};
                        min-width: 60px;
                    }}
                    QPushButton:hover {{
                        background: white;
                        border-color: {self.color_profile.gradient_end_color.darker(115).name()};
                        color: {self.color_profile.gradient_end_color.darker(110).name()};
                    }}
                    QPushButton:checked {{
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 {self.color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.color_profile.gradient_end_color.lighter(110).name()});
                        border-color: {self.color_profile.gradient_end_color.darker(110).name()};
                        color: white;
                    }}
                                 """)
    def add_tag_button(self):
        tag_text = self.enter_string_dialog.line_edit.text()
        if tag_text not in self.tags:
            self.tags.add(tag_text)
            button = QPushButton(self)
            button.setText(tag_text)
            button.setCheckable(True)  # Make tags selectable
            self.tag_button_set_styling(button)
            self.ui.verticalLayout.addWidget(button)
            self.tag_buttons.append(button)
            self.tag_buttons[-1].clicked.connect(self.update_status_bar)
            
    def add_tag_clicked(self):
        self.sound_manager.play_click()
        self.create_enter_string_dialog('Enter tag: ', 'Add tag')
        self.enter_string_dialog.exec()
    def view_cards_clicked(self):
        """Show the view cards dialog"""
        logger.info("View cards button clicked")
        self.sound_manager.play_click()
        if not self.user:
            logger.warning("View cards attempted but user not authenticated")
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        logger.info(f"Opening view cards dialog for user: {self.user.email}")
        view_dialog = ViewCardsDialog(self.user, self)
        view_dialog.exec()
        logger.info("View cards dialog closed")
        
    def practice_clicked(self):
        """Start a practice session"""
        logger.info("Practice button clicked")
        self.sound_manager.play_click()
        if not self.user or not self.app:
            logger.warning("Practice attempted but user not authenticated")
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        logger.info(f"Starting practice session for user: {self.user.email}")
        practice_dialog = PracticeDialog(self.user, self.app, self)
        if practice_dialog.cant_practice is False:
            logger.info("Practice dialog opened successfully")
            practice_dialog.exec()
        else:
            logger.warning("Practice session could not be started (no due cards)")
        
        # Update status bar after practice session
        logger.debug("Updating status bar after practice session")
        self.update_status_bar()
    
    def concept_connect_clicked(self):
        """Start a Concept Connect game session"""
        self.sound_manager.play_click()
        if not self.user:
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        concept_connect_dialog = ConceptConnectDialog(self.user, self)
        concept_connect_dialog.exec()
        
    def save_clicked(self):
        """Manual save/sync functionality"""
        logger.info("Manual save button clicked")
        if not self.user or not self.app:
            logger.warning("Save attempted but user not authenticated")
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        try:
            logger.info("Starting manual save operation")
            self.statusBar().showMessage("Saving... 💾", 2000)
            self.app.save_user()
            logger.info("Manual save completed successfully")
            self.statusBar().showMessage("Data saved successfully! ✅", 3000)
        except Exception as e:
            logger.error(f"Manual save failed: {str(e)}", exc_info=True)
            self.statusBar().showMessage("Save failed! ❌", 3000)
            QMessageBox.warning(self, "Error", f"Failed to save: {str(e)}")
            
    def closeEvent(self, event):
        """Handle application close event - auto-save before closing"""
        # Clean up answer worker thread
        if self.answer_worker and self.answer_worker.isRunning():
            self.answer_worker.quit()
            self.answer_worker.wait(3000)  # Wait up to 3 seconds for clean shutdown
            
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
        logger.info("Add card button clicked")
        if not self.user or not self.app:
            logger.warning("Add card attempted but user not authenticated")
            QMessageBox.warning(self, "Error", "User not authenticated.")
            return
            
        try:
            # Get question and answer from text fields
            question = self.ui.CardDescriptionTextEdit.toPlainText().strip()
            answer = self.ui.textEdit.toPlainText().strip()
            logger.debug(f"Card input - Question length: {len(question)}, Answer length: {len(answer)}")
            
            if not question or not answer:
                logger.warning("Add card attempted with empty question or answer")
                QMessageBox.warning(self, "Error", "Please enter both question and answer.")
                return
                
            # Get selected tags
            selected_tags = set()
            for button in self.tag_buttons:
                if button.isChecked():
                    selected_tags.add(button.text())
            logger.debug(f"Selected tags for new card: {selected_tags}")
                    
            # Create new card
            card = Card()
            full_card = FullCard(card, question, answer, selected_tags)
            logger.debug(f"Created new FullCard with {len(selected_tags)} tags")
            
            # Add to user's cards
            if self.user and hasattr(self.user, 'full_cards'):
                self.user.full_cards.append(full_card)
                logger.info(f"Card added to user's collection. Total cards: {len(self.user.full_cards)}")
            else:
                logger.error("User object missing or invalid")
                QMessageBox.warning(self, "Error", "User data is invalid.")
                return
            
            # Save to database
            logger.info("Saving user data to database")
            self.app.save_user()
            logger.info("User data saved successfully")
            
            # Play success sound
            self.sound_manager.play_success()
            
            # Clear fields
            self.ui.CardDescriptionTextEdit.clear()
            self.ui.textEdit.clear()
            logger.debug("Input fields cleared")
            
            # Uncheck all tags
            for button in self.tag_buttons:
                button.setChecked(False)
            logger.debug("All tag buttons unchecked")
                
            self.statusBar().showMessage("Card added successfully! 🎉", 3000)
            # Update status bar with new card count after a delay
            self.update_status_bar()
            
        except Exception as e:
            logger.error(f"Error adding card: {str(e)}", exc_info=True)
            self.sound_manager.play_error()
            QMessageBox.warning(self, "Error", f"Failed to add card: {str(e)}")

    def connect_buttons_to_update_status_bar(self):
        for i in range(len(self.tag_buttons)):
            self.tag_buttons[i].clicked.connect(self.update_status_bar)

    def first_color_selected(self):
        self.color_profile.gradient_end_color = self.first_color_dialog.selectedColor()
        self.setup_modern_styling()
        for btn in self.tag_buttons:
            self.tag_button_set_styling(btn)
        self.set_generate_button_styling()

    def first_color_action_clicked(self):
        self.first_color_dialog = QColorDialog(self)
        self.first_color_dialog.colorSelected.connect(self.first_color_selected)
        self.first_color_dialog.show()
    
    def second_color_selected(self):
        self.color_profile.main_color = self.second_color_dialog.selectedColor()
        self.setup_modern_styling()
        for btn in self.tag_buttons:
            self.tag_button_set_styling(btn)
        self.set_generate_button_styling()

    def second_color_action_clicked(self):
        self.second_color_dialog = QColorDialog(self)
        self.second_color_dialog.colorSelected.connect(self.second_color_selected)
        self.second_color_dialog.show()
    
    def delete_tag_button_clicked(self):
        to_delete_names = self.get_selected_tags() 
        for button in self.tag_buttons[:]:
            text = button.text().strip()
            if text in to_delete_names:
                idx = self.ui.verticalLayout.indexOf(button)
                if idx != -1:
                    item = self.ui.verticalLayout.takeAt(idx)
                    w = item.widget()
                    if w:
                        w.setParent(None)
                        w.deleteLater()
                self.tag_buttons.remove(button)
        for card in self.user.full_cards:
            card.tags = card.tags - to_delete_names

        self.tags -= to_delete_names

def main():
    app = QApplication()
    window = MainWindow()
    if window.user:  # Only show if authentication was successful
        window.show()
        app.exec()

if __name__ == "__main__":
    main()
