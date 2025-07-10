from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QWidget, QFrame, QMessageBox, 
                              QScrollArea, QGridLayout, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, QParallelAnimationGroup, QSequentialAnimationGroup
from PySide6.QtGui import QFont, QColor, QPalette
import random
import math
from base_classes import FullCard

class CardWidget(QFrame):
    """Simple clickable card widget with animations"""
    def __init__(self, full_card, parent=None, card_type="question"):
        super().__init__(parent)
        self.full_card = full_card
        self.card_type = card_type  # "question" or "answer"
        self.selected = False
        self.matched = False
        self.parent_dialog = parent
        self.animation = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(200, 120)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Just show the content - question or answer
        if self.card_type == "question":
            content_text = self.full_card.question[:120] + "..." if len(self.full_card.question) > 120 else self.full_card.question
        else:
            content_text = self.full_card.answer[:120] + "..." if len(self.full_card.answer) > 120 else self.full_card.answer
        
        # Single text label that actually works
        self.text_label = QLabel(content_text)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
                background: transparent;
            }
        """)
        layout.addWidget(self.text_label)
        
        self.update_style()
        
    def update_style(self):
        """Update visual style based on state with smooth color transitions"""
        if self.matched:
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #2ecc71, stop: 1 #27ae60);
                    border: 3px solid #229954;
                    border-radius: 12px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                QLabel {
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    background: transparent;
                }
            """)
        elif self.selected:
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #3498db, stop: 1 #2980b9);
                    border: 3px solid #1f5582;
                    border-radius: 12px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                QLabel {
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    background: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #ffffff, stop: 1 #f8f9fa);
                    border: 2px solid #bdc3c7;
                    border-radius: 12px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                QFrame:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #ecf0f1, stop: 1 #d5dbdb);
                    border-color: #95a5a6;
                }
                QLabel {
                    color: #2c3e50;
                    font-weight: bold;
                    font-size: 12px;
                    background: transparent;
                }
            """)
            
    def animate_selection(self):
        """Animate card selection with a bounce effect"""
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        # Get current geometry
        current_rect = self.geometry()
        
        # Create a slightly smaller rect for the "pressed" effect
        smaller_rect = QRect(
            current_rect.x() + 3,
            current_rect.y() + 3,
            current_rect.width() - 6,
            current_rect.height() - 6
        )
        
        # Animate to smaller then back to normal
        self.animation.setStartValue(current_rect)
        self.animation.setKeyValueAt(0.5, smaller_rect)
        self.animation.setEndValue(current_rect)
        self.animation.start()
        
    def animate_match(self):
        """Smooth match animation with satisfying feedback"""
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        current_rect = self.geometry()
        larger_rect = QRect(
            current_rect.x() - 6,
            current_rect.y() - 6,
            current_rect.width() + 12,
            current_rect.height() + 12
        )
        
        self.animation.setStartValue(current_rect)
        self.animation.setKeyValueAt(0.7, larger_rect)
        self.animation.setEndValue(current_rect)
        self.animation.start()
        
    def animate_wrong_match(self):
        """Quick shake animation for wrong matches"""
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        original_rect = self.geometry()
        shake_distance = 5
        
        self.animation.setStartValue(original_rect)
        self.animation.setKeyValueAt(0.25, QRect(original_rect.x() + shake_distance, original_rect.y(), 
                                               original_rect.width(), original_rect.height()))
        self.animation.setKeyValueAt(0.75, QRect(original_rect.x() - shake_distance, original_rect.y(), 
                                               original_rect.width(), original_rect.height()))
        self.animation.setEndValue(original_rect)
        self.animation.start()
        
    def animate_entrance(self):
        """Simple entrance animation"""
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        current_rect = self.geometry()
        start_rect = QRect(current_rect.x(), current_rect.y() + 20, 
                          current_rect.width(), current_rect.height())
        
        self.setGeometry(start_rect)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(current_rect)
        self.animation.start()
        
    def animate_selection_bounce(self):
        """Quick bounce for selection"""
        if self.animation:
            self.animation.stop()
            
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        current_rect = self.geometry()
        bounce_rect = QRect(current_rect.x(), current_rect.y() - 5,
                           current_rect.width(), current_rect.height())
        
        self.animation.setStartValue(current_rect)
        self.animation.setKeyValueAt(0.5, bounce_rect)
        self.animation.setEndValue(current_rect)
        self.animation.start()
            
    def mousePressEvent(self, event):
        """Handle mouse clicks"""
        if event.button() == Qt.MouseButton.LeftButton and not self.matched:
            self.animate_selection_bounce()
            if self.parent_dialog:
                self.parent_dialog.card_clicked(self)
        super().mousePressEvent(event)

class ConceptConnectDialog(QDialog):
    """Simple card matching game"""
    
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.color_profile = getattr(parent, 'color_profile', None)
        self.selected_cards = []
        self.card_widgets = []
        self.matched_pairs = []
        self.game_cards = []
        self.score = 0
        self.matches_found = 0
        self.attempts = 0
        self.score_animation = None
        self.setup_ui()
        self.load_game_cards()
        
    def setup_ui(self):
        self.setWindowTitle("Concept Connect - Match Related Cards")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        # Apply color profile styling like other dialogs
        if self.color_profile:
            self.setStyleSheet(f"""
                QDialog {{
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 {self.color_profile.main_color.name()}, stop: 1 {self.color_profile.gradient_end_color.name()});
                    color: white;
                }}
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #6a1b9a, stop: 1 #8e24aa);
                    color: white;
                }
            """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("🎯 Concept Connect")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Instructions
        instructions_label = QLabel("Match questions with their answers! Find 4 pairs to win.")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setStyleSheet("font-size: 14px; color: white; margin: 10px;")
        main_layout.addWidget(instructions_label)
        
        # Score display
        self.score_label = QLabel("Score: 0 | Matches: 0 | Attempts: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: white; 
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        """)
        main_layout.addWidget(self.score_label)
        
        # Game area
        game_widget = QWidget()
        game_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        game_layout = QVBoxLayout(game_widget)
        
        self.cards_area = QWidget()
        self.cards_layout = QGridLayout(self.cards_area)
        self.cards_layout.setSpacing(15)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.cards_area)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        game_layout.addWidget(scroll_area)
        main_layout.addWidget(game_widget)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        hint_btn = QPushButton("💡 Hint")
        hint_btn.clicked.connect(self.show_hint)
        hint_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
            QPushButton:hover {
                background: white;
                border-color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background: rgba(240, 240, 240, 0.9);
            }
        """)
        buttons_layout.addWidget(hint_btn)
        
        new_game_btn = QPushButton("🔄 New Game")
        new_game_btn.clicked.connect(self.reset_game)
        new_game_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
            QPushButton:hover {
                background: white;
                border-color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background: rgba(240, 240, 240, 0.9);
            }
        """)
        buttons_layout.addWidget(new_game_btn)
        
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                color: #333;
                font-size: 14px;
            }
            QPushButton:hover {
                background: white;
                border-color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:pressed {
                background: rgba(240, 240, 240, 0.9);
            }
        """)
        buttons_layout.addWidget(close_btn)
        
        main_layout.addLayout(buttons_layout)
        
    def load_game_cards(self):
        """Load cards for the game, ensuring winnable pairs"""
        if not self.user or not self.user.full_cards:
            QMessageBox.warning(self, "No Cards", "You need to create some flashcards first!")
            self.close()
            return
            
        if len(self.user.full_cards) < 5:
            QMessageBox.warning(self, "Not Enough Cards", "You need at least 5 cards to play!")
            self.close()
            return
            
        # Create guaranteed matchable pairs
        self.game_cards = self.create_winnable_game()
            
        self.display_cards()
        
    def create_winnable_game(self):
        """Create a game with guaranteed Q&A pairs"""
        available_cards = self.user.full_cards.copy()
        random.shuffle(available_cards)
        
        # Create question-answer pairs from the same flashcards
        game_data = []
        
        # Create 4 complete pairs (8 cards) + 1 extra to make 9
        for card in available_cards[:4]:
            game_data.append((card, "question"))
            game_data.append((card, "answer"))
        
        # Add one more question if we have more cards available
        if len(available_cards) > 4:
            game_data.append((available_cards[4], "question"))
        
        # Shuffle so questions and answers aren't predictably placed
        random.shuffle(game_data)
        
        return game_data  # Return all 9 cards
        

        
    def display_cards(self):
        """Display cards in a grid with smooth entrance animations"""
        # Clear existing widgets
        for widget in self.card_widgets:
            widget.setParent(None)
        self.card_widgets.clear()
        
        # Add cards to grid - 3x3 layout for 9 cards
        cols = 3
        for i, (full_card, card_type) in enumerate(self.game_cards):
            row = i // cols
            col = i % cols
            
            card_widget = CardWidget(full_card, self, card_type)
            self.card_widgets.append(card_widget)
            self.cards_layout.addWidget(card_widget, row, col)
            
            # Animate entrance with staggered delays
            delay = i * 80  # 80ms delay between each card
            QTimer.singleShot(delay, card_widget.animate_entrance)
            
        # Add some stretch to center the cards nicely
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
    def card_clicked(self, card_widget):
        """Handle card selection with smooth animations"""
        if card_widget.matched:
            return
            
        if card_widget in self.selected_cards:
            # Deselect card
            card_widget.selected = False
            self.selected_cards.remove(card_widget)
        else:
            # Select card
            if len(self.selected_cards) >= 2:
                # Deselect previous selections with animation
                for card in self.selected_cards:
                    card.selected = False
                    card.update_style()
                self.selected_cards.clear()
                
            card_widget.selected = True
            self.selected_cards.append(card_widget)
            
        card_widget.update_style()
        
        # Check for match if 2 cards selected (with slight delay for better UX)
        if len(self.selected_cards) == 2:
            QTimer.singleShot(200, self.check_match)
            
    def check_match(self):
        """Check if selected cards match"""
        if len(self.selected_cards) != 2:
            return
            
        card1, card2 = self.selected_cards
        self.attempts += 1
        
        # Enhanced matching logic
        is_match = self.cards_are_related(card1, card2)
        
        if is_match:
            # Match found - animate success!
            self.matches_found += 1
            self.score += 100
            
            card1.matched = True
            card2.matched = True
            card1.selected = False
            card2.selected = False
            
            # Animate the successful match
            card1.animate_match()
            card2.animate_match()
            
            # Update styles after a short delay to show animation
            QTimer.singleShot(100, lambda: self.update_matched_cards([card1, card2]))
            
            # Show success message with match reason
            match_reason = self.get_match_reason(card1, card2)
            QTimer.singleShot(500, lambda: QMessageBox.information(self, "Match! 🎉", 
                f"Perfect match! +100 points\n\n{match_reason}\n\nScore: {self.score}"))
            
            # Check if game complete (4 matches for 9 cards with 8 matchable)
            if self.matches_found >= 4:
                QTimer.singleShot(1000, self.game_complete)
                
        else:
            # No match - animate rejection
            self.score = max(0, self.score - 20)
            
            # Brief pause then show no match
            QTimer.singleShot(300, lambda: self.handle_no_match(card1, card2))
                
        self.selected_cards.clear()
        self.update_score_display()
        
    def update_matched_cards(self, cards):
        """Update the styling of matched cards"""
        for card in cards:
            card.update_style()
            
    def handle_no_match(self, card1, card2):
        """Handle when cards don't match with quick feedback"""
        # Animate the wrong match
        card1.animate_wrong_match()
        card2.animate_wrong_match()
        
        # Show message and deselect cards
        QTimer.singleShot(200, lambda: QMessageBox.information(self, "No Match", 
            f"These cards don't match. -20 points\n\nScore: {self.score}"))
        
        # Deselect cards
        card1.selected = False
        card2.selected = False
        card1.update_style()
        card2.update_style()
        
    def get_match_reason(self, card1_widget, card2_widget):
        """Get the reason why two card widgets match"""
        # For Q&A pairs, the reason is always the same
        if card1_widget.card_type == "question":
            return f"Question matches its Answer!"
        else:
            return f"Answer matches its Question!"
        
    def cards_are_related(self, card1_widget, card2_widget):
        """Check if two card widgets are a matching Q&A pair"""
        # Cards match if they're from the same flashcard but different types (Q&A pair)
        return (card1_widget.full_card == card2_widget.full_card and 
                card1_widget.card_type != card2_widget.card_type)
        
    def update_score_display(self):
        """Update score display with simple animation"""
        self.score_label.setText(f"Score: {self.score} | Matches: {self.matches_found} | Attempts: {self.attempts}")
        
        # Quick bounce animation
        if self.score_animation:
            self.score_animation.stop()
            
        self.score_animation = QPropertyAnimation(self.score_label, b"geometry")
        self.score_animation.setDuration(200)
        self.score_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        current_rect = self.score_label.geometry()
        bounce_rect = QRect(current_rect.x(), current_rect.y() - 2,
                           current_rect.width(), current_rect.height())
        
        self.score_animation.setStartValue(current_rect)
        self.score_animation.setKeyValueAt(0.5, bounce_rect)
        self.score_animation.setEndValue(current_rect)
        self.score_animation.start()
        
    def show_hint(self):
        """Show a hint with better guidance"""
        unmatched_cards = [card for card in self.card_widgets if not card.matched]
        if len(unmatched_cards) < 2:
            QMessageBox.information(self, "Hint", "Almost done! Keep going!")
            return
            
        # Find a potential Q&A match and explain why
        for i, card1 in enumerate(unmatched_cards):
            for j, card2 in enumerate(unmatched_cards[i+1:], i+1):
                if self.cards_are_related(card1, card2):
                    # Show the question and answer content for the hint
                    if card1.card_type == "question":
                        question_card, answer_card = card1, card2
                    else:
                        question_card, answer_card = card2, card1
                    
                    QMessageBox.information(self, "Hint 💡", 
                        f"Try matching this Question with its Answer:\n\n"
                        f"❓ Question: {question_card.full_card.question[:50]}...\n\n"
                        f"💡 Answer: {answer_card.full_card.answer[:50]}...\n\n"
                        f"These cards are from the same flashcard!")
                    return
                    
        QMessageBox.information(self, "Hint", 
            "Look for Questions and Answers that belong together!\n\n"
            "Most questions have their matching answers in the game.\n"
            "Find 4 pairs to win!")
        
    def game_complete(self):
        """Handle game completion with simple celebration"""
        accuracy = (self.matches_found / self.attempts * 100) if self.attempts > 0 else 0
        
        # Quick celebration bounce for all matched cards
        for card in self.card_widgets:
            if card.matched:
                card.animate_match()
        
        # Show completion message
        QTimer.singleShot(300, lambda: QMessageBox.information(self, "Game Complete! 🎉", 
            f"Congratulations! You won!\n\n"
            f"Final Score: {self.score}\n"
            f"Matches: {self.matches_found}\n"
            f"Attempts: {self.attempts}\n"
            f"Accuracy: {accuracy:.1f}%\n\n"
            f"Great job connecting your flashcards!"))
        
    def reset_game(self):
        """Reset the game"""
        self.selected_cards.clear()
        self.matched_pairs.clear()
        self.score = 0
        self.matches_found = 0
        self.attempts = 0
        
        # Reset all cards
        for card in self.card_widgets:
            card.selected = False
            card.matched = False
            card.update_style()
        
        self.update_score_display()
        self.load_game_cards()  # Load new random cards 