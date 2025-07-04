from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QWidget, QFrame, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt
from datetime import datetime, timezone
from fsrs import Rating
from base_classes import FullCard

class PracticeDialog(QDialog):
    def __init__(self, user, app, parent=None):
        super().__init__(parent)
        self.user = user
        self.app = app
        self.current_card_index = 0
        self.due_cards = []
        self.review_logs = []
        self.cards_reviewed = 0
        self.setup_ui()
        self.load_due_cards()
        
    def setup_ui(self):
        self.setWindowTitle("Practice - Spaced Repetition")
        self.setFixedSize(700, 500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Header with progress
        self.header_label = QLabel()
        self.header_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(self.header_label)
        
        # Card container
        self.card_frame = QFrame()
        self.card_frame.setFrameStyle(QFrame.Shape.Box)
        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(self.card_frame)
        
        # Question
        self.question_label = QLabel("Question:")
        self.question_label.setStyleSheet("font-weight: bold; color: #007bff; font-size: 14px;")
        card_layout.addWidget(self.question_label)
        
        self.question_text = QLabel()
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("""
            background-color: white; 
            padding: 15px; 
            border-radius: 8px; 
            border: 1px solid #ced4da;
            font-size: 16px;
            min-height: 80px;
        """)
        card_layout.addWidget(self.question_text)
        
        # Show Answer button
        self.show_answer_btn = QPushButton("Show Answer")
        self.show_answer_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.show_answer_btn.clicked.connect(self.show_answer)
        card_layout.addWidget(self.show_answer_btn)
        
        # Answer (initially hidden)
        self.answer_label = QLabel("Answer:")
        self.answer_label.setStyleSheet("font-weight: bold; color: #28a745; font-size: 14px; margin-top: 10px;")
        self.answer_label.setVisible(False)
        card_layout.addWidget(self.answer_label)
        
        self.answer_text = QLabel()
        self.answer_text.setWordWrap(True)
        self.answer_text.setStyleSheet("""
            background-color: white; 
            padding: 15px; 
            border-radius: 8px; 
            border: 1px solid #ced4da;
            font-size: 16px;
            min-height: 80px;
        """)
        self.answer_text.setVisible(False)
        card_layout.addWidget(self.answer_text)
        
        # Rating buttons (initially hidden)
        self.rating_widget = QWidget()
        rating_layout = QVBoxLayout(self.rating_widget)
        
        rating_instruction = QLabel("How well did you remember this card?")
        rating_instruction.setStyleSheet("font-weight: bold; text-align: center; margin: 10px;")
        rating_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rating_layout.addWidget(rating_instruction)
        
        buttons_layout = QHBoxLayout()
        
        # Again button (Rating.Again = 1)
        self.again_btn = QPushButton("Again\n(Forgot)")
        self.again_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.again_btn.clicked.connect(lambda: self.rate_card(Rating.Again))
        buttons_layout.addWidget(self.again_btn)
        
        # Hard button (Rating.Hard = 2)
        self.hard_btn = QPushButton("Hard\n(Difficult)")
        self.hard_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e8690b;
            }
        """)
        self.hard_btn.clicked.connect(lambda: self.rate_card(Rating.Hard))
        buttons_layout.addWidget(self.hard_btn)
        
        # Good button (Rating.Good = 3)
        self.good_btn = QPushButton("Good\n(Hesitated)")
        self.good_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.good_btn.clicked.connect(lambda: self.rate_card(Rating.Good))
        buttons_layout.addWidget(self.good_btn)
        
        # Easy button (Rating.Easy = 4)
        self.easy_btn = QPushButton("Easy\n(Perfect)")
        self.easy_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a359a;
            }
        """)
        self.easy_btn.clicked.connect(lambda: self.rate_card(Rating.Easy))
        buttons_layout.addWidget(self.easy_btn)
        
        rating_layout.addLayout(buttons_layout)
        self.rating_widget.setVisible(False)
        card_layout.addWidget(self.rating_widget)
        
        main_layout.addWidget(self.card_frame)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.finish_btn = QPushButton("Finish Practice")
        self.finish_btn.clicked.connect(self.finish_practice)
        bottom_layout.addWidget(self.finish_btn)
        
        main_layout.addLayout(bottom_layout)
        
    def load_due_cards(self):
        """Load cards that are due for review"""
        if not self.user.full_cards:
            QMessageBox.information(self, "No Cards", "You don't have any cards to practice. Create some cards first!")
            self.close()
            return
            
        now = datetime.now(timezone.utc)
        self.due_cards = []
        
        for full_card in self.user.full_cards:
            if full_card.card.due <= now:
                self.due_cards.append(full_card)
        
        if not self.due_cards:
            QMessageBox.information(self, "No Due Cards", "No cards are due for review right now. Great job staying on top of your studies!")
            self.close()
            return
            
        self.current_card_index = 0
        self.update_display()
        
    def update_display(self):
        """Update the display with current card"""
        if self.current_card_index >= len(self.due_cards):
            self.finish_practice()
            return
            
        current_card = self.due_cards[self.current_card_index]
        
        # Update header
        self.header_label.setText(f"Practice Session - Card {self.current_card_index + 1} of {len(self.due_cards)}")
        
        # Update question
        self.question_text.setText(current_card.question)
        
        # Update answer (but keep it hidden)
        self.answer_text.setText(current_card.answer)
        
        # Reset visibility
        self.show_answer_btn.setVisible(True)
        self.answer_label.setVisible(False)
        self.answer_text.setVisible(False)
        self.rating_widget.setVisible(False)
        
    def show_answer(self):
        """Show the answer and rating buttons"""
        self.show_answer_btn.setVisible(False)
        self.answer_label.setVisible(True)
        self.answer_text.setVisible(True)
        self.rating_widget.setVisible(True)
        
    def rate_card(self, rating):
        """Rate the current card and move to next"""
        current_card = self.due_cards[self.current_card_index]
        
        # Use FSRS to update the card
        try:
            updated_card, review_log = self.user.scheduler.review_card(current_card.card, rating)
            
            # Update the card in the full_card object
            current_card.card = updated_card
            
            # Store the review log
            self.user.review_logs.append(review_log)
            self.review_logs.append(review_log)
            
            self.cards_reviewed += 1
            
            # Move to next card
            self.current_card_index += 1
            self.update_display()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rate card: {str(e)}")
            
    def finish_practice(self):
        """Finish the practice session"""
        if self.cards_reviewed > 0:
            try:
                # Save updated user data
                self.app.save_user()
                
                QMessageBox.information(self, "Practice Complete", 
                    f"Great job! You reviewed {self.cards_reviewed} cards.\n\n"
                    f"Your progress has been saved.")
            except Exception as e:
                QMessageBox.warning(self, "Save Error", f"Failed to save progress: {str(e)}")
        else:
            QMessageBox.information(self, "Practice Complete", "No cards were reviewed.")
            
        self.accept() 