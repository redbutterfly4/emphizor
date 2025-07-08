from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QScrollArea, QWidget, QFrame, QTextEdit)
from PySide6.QtCore import Qt
from base_classes import FullCard
from ColorProfile import ColorProfile

class ViewCardsDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        # Get color profile from parent if available, otherwise create default
        self.color_profile = getattr(parent, 'color_profile', ColorProfile())
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Your Flashcard Collection")
        self.resize(900, 700)
        self.setMinimumSize(500, 350)  # Better minimum for small screens
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply modern styling with purple theme like practice UI
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                color: white;
            }}
            QScrollArea {{
                border: none;
                border-radius: 15px;
            }}
            QScrollArea QWidget {{
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.parent().color_profile.gradient_end_color.darker(105)};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.parent().color_profile.gradient_end_color.lighter(105)};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QPushButton {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(110).name()});
                border: none;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px 30px;
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
        """)
        
        # Main layout with responsive spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Smaller margins for small screens
        main_layout.setSpacing(15)
        
        # Header section
        header_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Your Flashcard Collection")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Subtitle with count
        subtitle_label = QLabel(f"{self.user.name}'s Library • {len(self.user.full_cards)} cards")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 15px;
            }
        """)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container widget for cards
        cards_container = QWidget()
        cards_layout = QVBoxLayout(cards_container)
        cards_layout.setSpacing(10)  # Smaller spacing for mobile
        cards_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add each card as a widget
        if self.user.full_cards:
            for i, full_card in enumerate(self.user.full_cards):
                card_widget = self.create_card_widget(full_card, i + 1)
                cards_layout.addWidget(card_widget)
        else:
            # No cards message
            no_cards_widget = QFrame()
            no_cards_widget.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.1);
                    border: 2px dashed rgba(255, 255, 255, 0.3);
                    border-radius: 20px;
                    padding: 30px;
                    margin: 15px;
                }
            """)
            no_cards_layout = QVBoxLayout(no_cards_widget)
            
            no_cards_icon = QLabel("📚")
            no_cards_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_cards_icon.setStyleSheet("font-size: 48px; margin-bottom: 10px;")
            no_cards_layout.addWidget(no_cards_icon)
            
            no_cards_label = QLabel("No cards found")
            no_cards_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_cards_label.setStyleSheet("""
                color: white;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 5px;
            """)
            no_cards_layout.addWidget(no_cards_label)
            
            no_cards_hint = QLabel("Create some flashcards to get started!")
            no_cards_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_cards_hint.setStyleSheet("""
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                font-style: italic;
            """)
            no_cards_layout.addWidget(no_cards_hint)
            
            cards_layout.addWidget(no_cards_widget)
        
        # Add stretch to push cards to top
        cards_layout.addStretch()
        
        scroll_area.setWidget(cards_container)
        main_layout.addWidget(scroll_area)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 10px 25px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
                color: white;
            }
        """)
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn)
    def delete_card(self, card):
        self.user.full
    def create_card_widget(self, full_card: FullCard, card_number: int):
        """Create a widget for displaying a single card"""
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 20px;
                padding: 0px;
                margin: 3px;
            }
        """)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(20, 20, 20, 20)  # Responsive margins
        card_layout.setSpacing(12)
        
        # Card header with number
        header_layout = QHBoxLayout()
        
        number_label = QLabel(f"Card #{card_number}")
        number_label.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.parent().color_profile.gradient_end_color.darker(130).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(110).name()});
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 6px 12px;
                border-radius: 12px;
            }}
        """)
        header_layout.addWidget(number_label)
        header_layout.addStretch()
        delete_card_button = QPushButton(self)
        delete_card_button.setText('Delete card')
        header_layout.addWidget(delete_card_button)
        delete_card_button.clicked.connect(lambda card: self.delete_card(card))
        
        card_layout.addLayout(header_layout)
        
        # Question section
        question_label = QLabel("Question")
        question_label.setStyleSheet(f"""
            QLabel {{
                color: {self.parent().color_profile.gradient_end_color.darker(130).name()};
                font-weight: bold;
                font-size: 14px;
                margin-bottom: 3px;
            }}
        """)
        card_layout.addWidget(question_label)
        
        question_text = QLabel(full_card.question)
        question_text.setWordWrap(True)
        question_text.setStyleSheet(f"""
            QLabel {{
                background: #fff;
                border: 2px solid {self.parent().color_profile.gradient_end_color.darker(115).name()};
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
                line-height: 1.4;
                color: {self.parent().color_profile.gradient_end_color.darker(120).name()};
                min-height: 30px;
            }}
        """)
        card_layout.addWidget(question_text)
        
        # Answer section
        answer_label = QLabel("Answer")
        answer_label.setStyleSheet(f"""
            QLabel {{
                color: {self.parent().color_profile.gradient_end_color.darker(105).name()};
                font-weight: bold;
                font-size: 14px;
                margin-bottom: 3px;
            }}
        """)
        card_layout.addWidget(answer_label)
        
        answer_text = QLabel(full_card.answer)
        answer_text.setWordWrap(True)
        answer_text.setStyleSheet(f"""
            QLabel {{
                background: #fff;
                border: 2px solid {self.parent().color_profile.gradient_end_color.darker(115).name()};
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
                line-height: 1.4;
                color: {self.parent().color_profile.gradient_end_color.darker(120).name()};
                min-height: 30px;
            }}
        """)
        card_layout.addWidget(answer_text)
        
        # Tags section
        if full_card.tags:
            tags_label = QLabel("Tags")
            tags_label.setStyleSheet(f"""
                QLabel {{
                    color: {self.parent().color_profile.gradient_end_color.lighter(90).name()};
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 3px;
                }}
            """)
            card_layout.addWidget(tags_label)
            
            tags_container = QWidget()
            tags_layout = QHBoxLayout(tags_container)
            tags_layout.setContentsMargins(0, 0, 0, 0)
            tags_layout.setSpacing(6)
            
            for tag in full_card.tags:
                tag_label = QLabel(tag)
                tag_label.setStyleSheet(f"""
                    QLabel {{
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 {self.parent().color_profile.gradient_end_color.darker(120).name()}, stop: 1 {self.parent().color_profile.gradient_end_color.lighter(130).name()});
                        color: white;
                        padding: 4px 10px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 600;
                    }}
                """)
                tags_layout.addWidget(tag_label)
            
            tags_layout.addStretch()
            card_layout.addWidget(tags_container)
        
        return card_frame 