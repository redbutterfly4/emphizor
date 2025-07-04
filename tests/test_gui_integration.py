"""
Integration tests for Emphizor GUI components.
"""

import pytest
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

# Import Qt modules
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from base_classes import App, User, FullCard
from fsrs import Card, Scheduler, Rating


class TestGUIIntegration:
    """Test GUI integration with the application"""

    @pytest.fixture(autouse=True)
    def setup_qt_app(self):
        """Setup Qt application for GUI tests"""
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        yield
        # Cleanup is handled by Qt

    @pytest.mark.integration
    @pytest.mark.gui
    def test_auth_dialog_integration(self, test_env, mock_supabase):
        """Test authentication dialog integration"""
        from AuthDialog import AuthDialog
        
        # Mock the app creation
        with patch('AuthDialog.App') as mock_app_class:
            mock_app_instance = MagicMock()
            mock_app_instance.supabase = mock_supabase
            mock_app_class.return_value = mock_app_instance
            
            # Mock successful login
            mock_supabase.table.return_value.execute.return_value = MagicMock(data=[{
                'id': 1,
                'name': test_env['name'],
                'email': test_env['email'],
                'full_cards': [],
                'review_logs': [],
                'scheduler': Scheduler().to_dict()
            }])
            
            # Create dialog
            dialog = AuthDialog(None)
            
            # Simulate user input
            dialog.signin_email.setText(test_env['email'])
            dialog.signin_password.setText(test_env['password'])
            
            # Test login
            dialog.sign_in()
            
            # Verify app was created and user was set
            mock_app_class.assert_called_once()
            assert dialog.app is not None
            assert dialog.user is not None

    @pytest.mark.integration
    @pytest.mark.gui
    def test_main_window_initialization(self, test_env, mock_supabase):
        """Test main window initialization with authenticated user"""
        from gui import MainWindow
        
        # Mock the authentication dialog
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            # Create mock app and user
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Verify window was initialized correctly
            assert window.app is not None
            assert window.user is not None
            assert window.user.email == test_env['email']
            assert window.user.name == test_env['name']

    @pytest.mark.integration
    @pytest.mark.gui
    def test_add_card_functionality(self, test_env, mock_supabase):
        """Test adding cards through the GUI"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Set up card data
            question = "What is integration testing?"
            answer = "Testing that verifies the interfaces between components"
            
            # Fill in the form
            window.ui.CardDescriptionTextEdit.setPlainText(question)
            window.ui.textEdit.setPlainText(answer)
            
            # Initial card count
            initial_count = len(window.user.full_cards)
            
            # Add card
            window.add_card_clicked()
            
            # Verify card was added
            assert len(window.user.full_cards) == initial_count + 1
            new_card = window.user.full_cards[-1]
            assert new_card.question == question
            assert new_card.answer == answer
            
            # Verify form was cleared
            assert window.ui.CardDescriptionTextEdit.toPlainText() == ""
            assert window.ui.textEdit.toPlainText() == ""

    @pytest.mark.integration
    @pytest.mark.gui
    def test_tag_management(self, test_env, mock_supabase):
        """Test tag management functionality"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Mock the EnterStringDialog
            with patch('gui.EnterStringDialog') as mock_dialog:
                mock_dialog_instance = MagicMock()
                mock_dialog_instance.line_edit.text.return_value = "test-tag"
                mock_dialog.return_value = mock_dialog_instance
                
                # Set up the accepted signal connection
                window.enter_string_dialog = mock_dialog_instance
                
                # Add a tag
                window.add_tag_button()
                
                # Verify tag was added
                assert "test-tag" in window.tags
                assert len(window.tag_buttons) > 0

    @pytest.mark.integration
    @pytest.mark.gui
    def test_view_cards_dialog(self, test_env, sample_cards, mock_supabase):
        """Test the view cards dialog functionality"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], sample_cards, [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Mock the ViewCardsDialog
            with patch('gui.ViewCardsDialog') as mock_view_dialog:
                mock_view_dialog_instance = MagicMock()
                mock_view_dialog.return_value = mock_view_dialog_instance
                
                # Test view cards
                window.view_cards_clicked()
                
                # Verify dialog was created and shown
                mock_view_dialog.assert_called_once_with(window.user, window)
                mock_view_dialog_instance.exec.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.gui
    def test_practice_dialog(self, test_env, due_cards, mock_supabase):
        """Test the practice dialog functionality"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], due_cards, [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Mock the PracticeDialog
            with patch('gui.PracticeDialog') as mock_practice_dialog:
                mock_practice_dialog_instance = MagicMock()
                mock_practice_dialog.return_value = mock_practice_dialog_instance
                
                # Test practice
                window.practice_clicked()
                
                # Verify dialog was created and shown
                mock_practice_dialog.assert_called_once_with(window.user, window.app, window)
                mock_practice_dialog_instance.exec.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.gui
    def test_save_functionality(self, test_env, mock_supabase):
        """Test the save functionality"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Test save
            window.save_clicked()
            
            # Verify save was called
            mock_app.save_user.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.gui
    def test_practice_dialog_complete_flow(self, test_env, due_cards, mock_supabase):
        """Test complete practice dialog flow"""
        from PracticeDialog import PracticeDialog
        
        # Create mock app and user
        mock_app = MagicMock()
        mock_app.supabase = mock_supabase
        mock_user = User(test_env['name'], test_env['email'], due_cards, [], Scheduler())
        
        # Create practice dialog
        dialog = PracticeDialog(mock_user, mock_app, None)
        
        # Verify dialog initialization
        assert dialog.user == mock_user
        assert dialog.app == mock_app
        assert len(dialog.due_cards) == len(due_cards)
        assert dialog.current_card_index == 0
        
        # Test showing answer
        dialog.show_answer()
        
        # Verify answer section is visible
        assert dialog.answer_container.isVisible()
        assert dialog.rating_section.isVisible()
        assert not dialog.show_answer_btn.isVisible()
        
        # Test rating a card
        initial_review_count = len(mock_user.review_logs)
        dialog.rate_card(Rating.Good)
        
        # Verify card was rated
        assert len(mock_user.review_logs) == initial_review_count + 1
        assert dialog.cards_reviewed == 1

    @pytest.mark.integration
    @pytest.mark.gui
    def test_view_cards_dialog_complete_flow(self, test_env, sample_cards):
        """Test complete view cards dialog flow"""
        from ViewCardsDialog import ViewCardsDialog
        
        # Create mock user with cards
        mock_user = User(test_env['name'], test_env['email'], sample_cards, [], Scheduler())
        
        # Create view cards dialog
        dialog = ViewCardsDialog(mock_user, None)
        
        # Verify dialog initialization
        assert dialog.user == mock_user
        assert len(dialog.user.full_cards) == len(sample_cards)
        
        # Test filtering (if implemented)
        # This would depend on the actual implementation of ViewCardsDialog

    @pytest.mark.integration
    @pytest.mark.gui
    def test_error_handling_in_gui(self, test_env, mock_supabase):
        """Test error handling in GUI components"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Test adding card with empty fields
            window.ui.CardDescriptionTextEdit.setPlainText("")
            window.ui.textEdit.setPlainText("")
            
            # Mock QMessageBox to avoid actual dialog
            with patch('gui.QMessageBox') as mock_msgbox:
                window.add_card_clicked()
                
                # Verify error message was shown
                mock_msgbox.warning.assert_called_once()
            
            # Test save error handling
            mock_app.save_user.side_effect = Exception("Save failed")
            
            with patch('gui.QMessageBox') as mock_msgbox:
                window.save_clicked()
                
                # Verify error message was shown
                mock_msgbox.warning.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.gui
    def test_window_close_with_auto_save(self, test_env, mock_supabase):
        """Test window close event with auto-save"""
        from gui import MainWindow
        from PySide6.QtGui import QCloseEvent
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], [], [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Create close event
            close_event = QCloseEvent()
            
            # Test close event
            window.closeEvent(close_event)
            
            # Verify save was called
            mock_app.save_user.assert_called_once()
            
            # Verify event was accepted
            assert close_event.isAccepted()

    @pytest.mark.integration
    @pytest.mark.gui
    def test_status_bar_updates(self, test_env, sample_cards, mock_supabase):
        """Test status bar updates"""
        from gui import MainWindow
        
        # Mock authentication
        with patch('gui.AuthDialog') as mock_auth_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog_instance.exec.return_value = QDialog.DialogCode.Accepted
            
            mock_app = MagicMock()
            mock_app.supabase = mock_supabase
            mock_user = User(test_env['name'], test_env['email'], sample_cards, [], Scheduler())
            
            mock_dialog_instance.get_app.return_value = mock_app
            mock_dialog_instance.get_user.return_value = mock_user
            mock_auth_dialog.return_value = mock_dialog_instance
            
            # Create main window
            window = MainWindow()
            
            # Test status bar update
            window.update_status_bar()
            
            # Verify status bar message contains user info
            status_text = window.statusBar().currentMessage()
            assert test_env['name'] in status_text
            assert str(len(sample_cards)) in status_text 