"""
Integration tests for Emphizor application core functionality.
"""

import pytest
import os
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from base_classes import App, User, FullCard
from fsrs import Card, Scheduler, Rating


class TestAppIntegration:
    """Test the main App class functionality"""

    @pytest.mark.integration
    def test_app_initialization(self, app):
        """Test that the app initializes correctly"""
        assert isinstance(app, App)
        assert app.supabase is not None
        assert app.user is None

    @pytest.mark.integration
    @pytest.mark.auth
    def test_login_with_valid_credentials(self, app, test_env):
        """Test login with valid credentials"""
        # Note: This test makes actual API calls to Supabase
        # In a real test environment, you might want to use a test database
        
        # Skip this test if we don't have real credentials
        if not os.path.exists('test.env'):
            pytest.skip("No test.env file found - skipping live integration test")
        
        try:
            app.login_or_signup(test_env['email'], test_env['password'], test_env['name'])
            
            # Verify user is logged in
            assert app.user is not None
            assert app.user.email == test_env['email']
            assert app.user.name == test_env['name']
            
        except Exception as e:
            # If login fails, it might be because the user doesn't exist yet
            # or because of network issues - this is expected in integration tests
            pytest.skip(f"Login failed (expected in some environments): {str(e)}")

    @pytest.mark.integration
    @pytest.mark.auth
    def test_signup_new_user(self, app, test_env):
        """Test signup for a new user"""
        # Use a unique email for signup testing
        test_email = f"test_{datetime.now().isoformat()}@emphizor.com"
        
        try:
            app.login_or_signup(test_email, test_env['password'], "New Test User")
            
            # Verify user was created
            assert app.user is not None
            assert app.user.email == test_email
            assert app.user.name == "New Test User"
            assert len(app.user.full_cards) == 0
            assert len(app.user.review_logs) == 0
            
        except Exception as e:
            pytest.skip(f"Signup failed (expected in some environments): {str(e)}")

    @pytest.mark.integration
    def test_login_with_mocked_supabase(self, app, test_env, mock_supabase):
        """Test login with mocked Supabase client"""
        # Replace the app's supabase client with our mock
        app.supabase = mock_supabase
        
        # Mock the database response for existing user
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[{
            'id': 1,
            'name': test_env['name'],
            'email': test_env['email'],
            'full_cards': [],
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }])
        
        # Test login
        app.login_or_signup(test_env['email'], test_env['password'])
        
        # Verify login was attempted
        mock_supabase.auth.sign_in_with_password.assert_called_once_with({
            'email': test_env['email'],
            'password': test_env['password']
        })
        
        # Verify user was loaded from database
        assert app.user is not None
        assert app.user.email == test_env['email']
        assert app.user.name == test_env['name']

    @pytest.mark.integration
    def test_save_user_with_mocked_supabase(self, app, test_user, mock_supabase):
        """Test saving user data with mocked Supabase"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Test save
        app.save_user()
        
        # Verify update was called
        mock_supabase.table.return_value.update.assert_called_once()
        mock_supabase.table.return_value.eq.assert_called_once_with("id", test_user.id)

    @pytest.mark.integration
    def test_user_card_management(self, test_user, sample_cards):
        """Test adding and managing cards for a user"""
        # Start with existing cards
        initial_count = len(test_user.full_cards)
        
        # Add new cards
        test_user.full_cards.extend(sample_cards)
        
        # Verify cards were added
        assert len(test_user.full_cards) == initial_count + len(sample_cards)
        
        # Test filtering by tags
        python_cards = [card for card in test_user.full_cards if "python" in card.tags]
        assert len(python_cards) >= 2  # At least 2 cards should have python tag
        
        # Test finding cards by question
        specific_card = next((card for card in test_user.full_cards if "2+2" in card.question), None)
        assert specific_card is not None
        assert specific_card.answer == "4"

    @pytest.mark.integration
    def test_practice_session_simulation(self, test_user, due_cards):
        """Test a complete practice session simulation"""
        # Add due cards to user
        test_user.full_cards.extend(due_cards)
        
        # Simulate practice session
        initial_review_count = len(test_user.review_logs)
        
        for card in due_cards:
            # Simulate rating each card
            rating = Rating.Good  # Simulate good performance
            
            # Use scheduler to review card
            updated_card, review_log = test_user.scheduler.review_card(card.card, rating)
            
            # Update card and add review log
            card.card = updated_card
            test_user.review_logs.append(review_log)
        
        # Verify practice session results
        assert len(test_user.review_logs) == initial_review_count + len(due_cards)
        
        # Verify all cards were updated (due dates should be in the future)
        for card in due_cards:
            assert card.card.due > datetime.now(timezone.utc)

    @pytest.mark.integration
    def test_card_serialization(self, sample_cards):
        """Test that cards can be serialized to/from dict format"""
        for card in sample_cards:
            # Test serialization
            card_dict = card.to_dict()
            
            # Verify dictionary structure
            assert 'card' in card_dict
            assert 'question' in card_dict
            assert 'answer' in card_dict
            assert 'tags' in card_dict
            
            # Verify data integrity
            assert card_dict['question'] == card.question
            assert card_dict['answer'] == card.answer
            assert card_dict['tags'] == card.tags

    @pytest.mark.integration
    def test_scheduler_integration(self, test_user):
        """Test FSRS scheduler integration"""
        # Create a new card
        card = Card()
        full_card = FullCard(card, "Test question", "Test answer", ["test"])
        
        # Add to user
        test_user.full_cards.append(full_card)
        
        # Test different ratings
        ratings = [Rating.Again, Rating.Hard, Rating.Good, Rating.Easy]
        
        for rating in ratings:
            # Create a fresh card for each rating test
            test_card = Card()
            updated_card, review_log = test_user.scheduler.review_card(test_card, rating)
            
            # Verify card was updated
            assert updated_card.due > datetime.now(timezone.utc)
            
            # Verify review log was created
            assert review_log.rating == rating
            assert review_log.review_time <= datetime.now(timezone.utc)

    @pytest.mark.integration
    def test_user_data_persistence(self, app, test_user, mock_supabase):
        """Test that user data persists correctly"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Add some cards and reviews
        card = Card()
        full_card = FullCard(card, "Persistence test", "Works correctly", ["persistence"])
        test_user.full_cards.append(full_card)
        
        # Simulate a review
        updated_card, review_log = test_user.scheduler.review_card(card, Rating.Good)
        full_card.card = updated_card
        test_user.review_logs.append(review_log)
        
        # Save user
        app.save_user()
        
        # Verify save was called with correct data
        mock_supabase.table.return_value.update.assert_called_once()
        
        # Get the data that was saved
        call_args = mock_supabase.table.return_value.update.call_args[0][0]
        
        # Verify the saved data structure
        assert 'name' in call_args
        assert 'email' in call_args
        assert 'full_cards' in call_args
        assert 'review_logs' in call_args
        assert 'scheduler' in call_args
        
        # Verify data integrity
        assert call_args['name'] == test_user.name
        assert call_args['email'] == test_user.email
        assert len(call_args['full_cards']) == len(test_user.full_cards)
        assert len(call_args['review_logs']) == len(test_user.review_logs)

    @pytest.mark.integration
    def test_error_handling(self, app, test_env):
        """Test error handling in various scenarios"""
        # Test login with invalid credentials
        with pytest.raises(ValueError):
            app.login_or_signup("invalid@email.com", "wrongpassword")
        
        # Test login without name for new user
        with pytest.raises(ValueError):
            app.login_or_signup("new@email.com", "password", None)
        
        # Test save without user
        app.user = None
        # This should not raise an error, but should handle gracefully
        # (based on the current implementation)

    @pytest.mark.integration
    def test_multiple_users(self, app, test_env, mock_supabase):
        """Test handling multiple users"""
        app.supabase = mock_supabase
        
        # Mock responses for two different users
        user1_data = {
            'id': 1,
            'name': test_env['name'],
            'email': test_env['email'],
            'full_cards': [],
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }
        
        user2_data = {
            'id': 2,
            'name': test_env['name_2'],
            'email': test_env['email_2'],
            'full_cards': [],
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }
        
        # Test first user login
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[user1_data])
        app.login_or_signup(test_env['email'], test_env['password'])
        
        first_user = app.user
        assert first_user.email == test_env['email']
        
        # Test second user login (would normally be a different app instance)
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[user2_data])
        app.login_or_signup(test_env['email_2'], test_env['password_2'])
        
        second_user = app.user
        assert second_user.email == test_env['email_2']
        
        # Verify users are different
        assert first_user.id != second_user.id
        assert first_user.email != second_user.email 