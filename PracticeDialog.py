from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QWidget, QFrame, QTextEdit, QMessageBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPalette, QColor
from datetime import datetime, timezone
from fsrs import Rating
from base_classes import FullCard
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)

class PracticeDialog(QDialog):
    def __init__(self, user, app, parent=None):
        super().__init__(parent)
        logger.info(f"Initializing PracticeDialog for user: {user.email}")
        self.user = user
        self.app = app
        self.current_card_index = 0
        self.due_cards = []
        self.review_logs = []
        self.cards_reviewed = 0
        self.cant_practice = False
        self.setup_ui()
        self.load_due_cards()
        logger.info(f"PracticeDialog initialized with {len(self.due_cards)} due cards")
        
    def setup_ui(self):
        self.setWindowTitle("Practice Session - Emphizor")
        self.resize(900, 700)
        self.setMinimumSize(500, 400)  # Better minimum for small screens
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply modern purple gradient styling like original practice UI
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.main_color.name()}, stop: 1 {self.parent().color_profile.gradient_end_color.name()});
                color: white;
            
            }}
        """)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)  # Smaller spacing for mobile
        main_layout.setContentsMargins(20, 20, 20, 20)  # Responsive margins
        
        # Header section
        header_layout = QVBoxLayout()
        
        # Progress and title
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
                padding: 10px;
            }
        """)
        header_layout.addWidget(self.progress_label)
        
        self.session_title = QLabel("Practice Session")
        self.session_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 0px 0px 20px 0px;
            }
        """)
        header_layout.addWidget(self.session_title)
        
        main_layout.addLayout(header_layout)
        
        # Card container - this is the main focal point
        self.card_container = QFrame()
        self.card_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                border: none;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
            }
        """)
        self.card_container.setMinimumHeight(250)  # Smaller for mobile
        
        card_layout = QVBoxLayout(self.card_container)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 30, 30, 30)  # Responsive margins
        
        # Question section
        self.question_container = QWidget()
        question_layout = QVBoxLayout(self.question_container)
        question_layout.setSpacing(12)
        
        self.question_label = QLabel("Question")
        self.question_label.setStyleSheet(f"""
            QLabel {{
                color: {self.parent().color_profile.main_color.name()}
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
        """)
        question_layout.addWidget(self.question_label)
        
        self.question_text = QLabel()
        self.question_text.setWordWrap(True)
        self.question_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.question_text.setStyleSheet(f"""
            QLabel {{
                background: {self.parent().color_profile.main_color.darker(105).name()};
                border: 2px solid {self.parent().color_profile.main_color.darker(115).name()};
                border-radius: 12px;
                padding: 20px;
                font-size: 18px;
                line-height: 1.4;
                color: #2d3748;
                min-height: 60px;
            }}
        """)
        question_layout.addWidget(self.question_text)
        
        card_layout.addWidget(self.question_container)
        
        # Answer section (initially hidden)
        self.answer_container = QWidget()
        self.answer_container.setVisible(False)
        answer_layout = QVBoxLayout(self.answer_container)
        answer_layout.setSpacing(12)
        
        self.answer_label = QLabel("Answer")
        self.answer_label.setStyleSheet("""
            QLabel {
                color: #48bb78;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        answer_layout.addWidget(self.answer_label)
        
        self.answer_text = QLabel()
        self.answer_text.setWordWrap(True)
        self.answer_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.answer_text.setStyleSheet("""
            QLabel {
                background: rgba(72, 187, 120, 0.1);
                border: 2px solid rgba(72, 187, 120, 0.2);
                border-radius: 12px;
                padding: 20px;
                font-size: 18px;
                line-height: 1.4;
                color: #2d3748;
                min-height: 60px;
            }
        """)
        answer_layout.addWidget(self.answer_text)
        
        card_layout.addWidget(self.answer_container)
        
        main_layout.addWidget(self.card_container)
        
        # Action section
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(15)
        
        # Show answer button
        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(110).name()});
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 40px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(110).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(120).name()});
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.lighter(110).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.darker(110).name()});
                }}
        """)
        self.show_answer_btn.clicked.connect(self.show_answer)
        actions_layout.addWidget(self.show_answer_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Rating section (initially hidden)
        self.rating_section = QWidget()
        self.rating_section.setVisible(False)
        rating_layout = QVBoxLayout(self.rating_section)
        rating_layout.setSpacing(15)
        
        # Rating instruction
        rating_instruction = QLabel("How well did you remember this card?")
        rating_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rating_instruction.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 10px;
            }
        """)
        rating_layout.addWidget(rating_instruction)
        
        # Rating buttons in a horizontal layout
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)  # Smaller spacing for mobile
        
        # Again button
        self.again_btn = QPushButton("Again")
        self.again_btn.setStyleSheet(self.get_rating_button_style("#ef4444", "#dc2626", "#b91c1c", "white"))
        self.again_btn.clicked.connect(lambda: self.rate_card(Rating.Again))
        buttons_layout.addWidget(self.again_btn)
        
        # Hard button
        self.hard_btn = QPushButton("Hard")
        self.hard_btn.setStyleSheet(self.get_rating_button_style("#f97316", "#ea580c", "#c2410c", "white"))
        self.hard_btn.clicked.connect(lambda: self.rate_card(Rating.Hard))
        buttons_layout.addWidget(self.hard_btn)
        
        # Good button
        self.good_btn = QPushButton("Good")
        self.good_btn.setStyleSheet(self.get_rating_button_style("#22c55e", "#16a34a", "#15803d", "white"))
        self.good_btn.clicked.connect(lambda: self.rate_card(Rating.Good))
        buttons_layout.addWidget(self.good_btn)
        
        # Easy button
        self.easy_btn = QPushButton("Easy")
        self.easy_btn.setStyleSheet(self.get_rating_button_style("#8b5cf6", "#7c3aed", "#6d28d9", "white"))
        self.easy_btn.clicked.connect(lambda: self.rate_card(Rating.Easy))
        buttons_layout.addWidget(self.easy_btn)
        
        rating_layout.addWidget(buttons_container)
        actions_layout.addWidget(self.rating_section)
        
        main_layout.addLayout(actions_layout)
        
        # Spacer to push everything up
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Bottom controls
        bottom_layout = QHBoxLayout()
        
        self.finish_btn = QPushButton("Finish Session")
        self.finish_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
            }
        """)
        self.finish_btn.clicked.connect(self.finish_practice)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.finish_btn)
        
        main_layout.addLayout(bottom_layout)
        
    def get_rating_button_style(self, primary, hover, pressed, text_color):
        return f"""
            QPushButton {{
                background: {primary};
                border: none;
                border-radius: 12px;
                color: {text_color};
                font-size: 14px;
                font-weight: bold;
                padding: 15px 20px;
                min-width: 60px;
                min-height: 15px;
            }}
            QPushButton:hover {{
                background: {hover};
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: {pressed};
                transform: translateY(0px);
            }}
        """
        
    def load_due_cards(self):
        """Load cards that are due for review"""
        if not self.user.full_cards:
            QMessageBox.information(self, "No Cards", "You don't have any cards to practice. Create some cards first!")
            self.cant_practice = True
            self.close()
            return
            
        now = datetime.now(timezone.utc)
        selected_tags = set()
        for button in self.parent().tag_buttons:
            if button.isChecked():
                selected_tags.add(button.text())
        self.due_cards = []
        
        for full_card in self.user.full_cards:
            if full_card.card.due <= now and full_card.tags <= selected_tags:
                self.due_cards.append(full_card)
        
        if not self.due_cards:
            QMessageBox.information(self, "No Due Cards", "No cards are due for review right now. Great job staying on top of your studies!")
            self.close()
            self.cant_practice = True
            return
            
        self.current_card_index = 0
        self.update_display()
        
    def update_display(self):
        """Update the display with current card"""
        if self.current_card_index >= len(self.due_cards):
            self.finish_practice()
            return
            
        current_card = self.due_cards[self.current_card_index]
        
        # Update progress
        self.progress_label.setText(f"Card {self.current_card_index + 1} of {len(self.due_cards)}")
        
        # Update question
        self.question_text.setText(current_card.question)
        
        # Update answer (but keep it hidden)
        self.answer_text.setText(current_card.answer)
        
        # Reset visibility
        self.show_answer_btn.setVisible(True)
        self.answer_container.setVisible(False)
        self.rating_section.setVisible(False)
        
    def show_answer(self):
        """Show the answer and rating buttons with animation"""
        self.show_answer_btn.setVisible(False)
        self.answer_container.setVisible(True)
        self.rating_section.setVisible(True)
        
    def rate_card(self, rating):
        """Rate the current card and move to next"""
        current_card = self.due_cards[self.current_card_index]
        logger.info(f"Rating card {self.current_card_index + 1} with rating: {rating}")
        
        # Use FSRS to update the card
        try:
            updated_card, review_log = self.user.scheduler.review_card(current_card.card, rating)
            
            # Update the card in the full_card object
            current_card.card = updated_card
            
            # Store the review log
            self.user.review_logs.append(review_log)
            self.review_logs.append(review_log)
            
            self.cards_reviewed += 1
            logger.info(f"Card rated successfully. Total cards reviewed: {self.cards_reviewed}")
            
            # Move to next card
            self.current_card_index += 1
            self.update_display()
            
        except Exception as e:
            logger.error(f"Failed to rate card: {str(e)}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to rate card: {str(e)}")
            
    def finish_practice(self):
        """Finish the practice session"""
        logger.info(f"Finishing practice session. Cards reviewed: {self.cards_reviewed}")
        if self.cards_reviewed > 0:
            try:
                # Save updated user data
                logger.info("Saving user data after practice session")
                self.app.save_user()
                logger.info("Practice session data saved successfully")
                
                QMessageBox.information(self, "Practice Complete", 
                    f"Excellent work! 🎉\n\nYou reviewed {self.cards_reviewed} cards.\n"
                    f"Your progress has been saved.\n\nKeep up the great studying!")
            except Exception as e:
                logger.error(f"Failed to save progress after practice: {str(e)}", exc_info=True)
                QMessageBox.warning(self, "Save Error", f"Failed to save progress: {str(e)}")
        else:
            logger.info("Practice session completed with no cards reviewed")
            QMessageBox.information(self, "Practice Complete", "No cards were reviewed.")
            
        self.accept() 