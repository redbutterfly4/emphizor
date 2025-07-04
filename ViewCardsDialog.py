from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QScrollArea, QWidget, QFrame, QTextEdit)
from PySide6.QtCore import Qt
from base_classes import FullCard

class ViewCardsDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("View Cards")
        self.setFixedSize(600, 500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(f"{self.user.name}'s Flashcards ({len(self.user.full_cards)} cards)")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Scroll area for cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container widget for cards
        cards_container = QWidget()
        cards_layout = QVBoxLayout(cards_container)
        
        # Add each card as a widget
        if self.user.full_cards:
            for i, full_card in enumerate(self.user.full_cards):
                card_widget = self.create_card_widget(full_card, i + 1)
                cards_layout.addWidget(card_widget)
        else:
            no_cards_label = QLabel("No cards found. Create some cards first!")
            no_cards_label.setStyleSheet("color: #666; font-style: italic; padding: 20px;")
            no_cards_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cards_layout.addWidget(no_cards_label)
        
        # Add stretch to push cards to top
        cards_layout.addStretch()
        
        scroll_area.setWidget(cards_container)
        main_layout.addWidget(scroll_area)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn)
        
    def create_card_widget(self, full_card: FullCard, card_number: int):
        """Create a widget for displaying a single card"""
        card_frame = QFrame()
        card_frame.setFrameStyle(QFrame.Shape.Box)
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }
        """)
        
        card_layout = QVBoxLayout(card_frame)
        
        # Card number
        number_label = QLabel(f"Card #{card_number}")
        number_label.setStyleSheet("font-weight: bold; color: #495057;")
        card_layout.addWidget(number_label)
        
        # Question
        question_label = QLabel("Question:")
        question_label.setStyleSheet("font-weight: bold; color: #007bff; margin-top: 10px;")
        card_layout.addWidget(question_label)
        
        question_text = QLabel(full_card.question)
        question_text.setWordWrap(True)
        question_text.setStyleSheet("background-color: white; padding: 8px; border-radius: 4px; border: 1px solid #ced4da;")
        card_layout.addWidget(question_text)
        
        # Answer
        answer_label = QLabel("Answer:")
        answer_label.setStyleSheet("font-weight: bold; color: #28a745; margin-top: 10px;")
        card_layout.addWidget(answer_label)
        
        answer_text = QLabel(full_card.answer)
        answer_text.setWordWrap(True)
        answer_text.setStyleSheet("background-color: white; padding: 8px; border-radius: 4px; border: 1px solid #ced4da;")
        card_layout.addWidget(answer_text)
        
        # Tags
        if full_card.tags:
            tags_label = QLabel("Tags:")
            tags_label.setStyleSheet("font-weight: bold; color: #6c757d; margin-top: 10px;")
            card_layout.addWidget(tags_label)
            
            tags_container = QWidget()
            tags_layout = QHBoxLayout(tags_container)
            tags_layout.setContentsMargins(0, 0, 0, 0)
            
            for tag in full_card.tags:
                tag_label = QLabel(tag)
                tag_label.setStyleSheet("""
                    background-color: #007bff;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 12px;
                """)
                tags_layout.addWidget(tag_label)
            
            tags_layout.addStretch()
            card_layout.addWidget(tags_container)
        
        return card_frame 