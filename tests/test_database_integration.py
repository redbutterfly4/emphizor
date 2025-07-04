"""
Database integration tests for Emphizor application.
"""

import pytest
import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from base_classes import App, User, FullCard
from fsrs import Card, Scheduler, Rating


class TestDatabaseIntegration:
    """Test database integration and data persistence"""

    @pytest.mark.integration
    @pytest.mark.database
    def test_user_creation_with_database(self, app, test_env, mock_supabase):
        """Test user creation with database operations"""
        app.supabase = mock_supabase
        
        # Mock successful signup
        mock_supabase.auth.sign_up.return_value = MagicMock(
            user={'id': 'test-id', 'email': test_env['email']}
        )
        
        # Mock empty database response (new user)
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[])
        
        # Test user creation
        app.login_or_signup(test_env['email'], test_env['password'], test_env['name'])
        
        # Verify user was created
        assert app.user is not None
        assert app.user.email == test_env['email']
        assert app.user.name == test_env['name']
        
        # Verify database insert was called
        mock_supabase.table.return_value.insert.assert_called_once()

    @pytest.mark.integration
    @pytest.mark.database
    def test_user_login_with_existing_data(self, app, test_env, mock_supabase):
        """Test user login with existing data in database"""
        app.supabase = mock_supabase
        
        # Mock successful login
        mock_supabase.auth.sign_in_with_password.return_value = MagicMock(
            user={'id': 'test-id', 'email': test_env['email']}
        )
        
        # Mock existing user data
        existing_cards = [
            {
                'card': Card().to_dict(),
                'question': 'Test Question',
                'answer': 'Test Answer',
                'tags': ['test']
            }
        ]
        
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[{
            'id': 1,
            'name': test_env['name'],
            'email': test_env['email'],
            'full_cards': existing_cards,
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }])
        
        # Test login
        app.login_or_signup(test_env['email'], test_env['password'])
        
        # Verify user was loaded with existing data
        assert app.user is not None
        assert app.user.email == test_env['email']
        assert app.user.name == test_env['name']
        assert len(app.user.full_cards) == 1
        assert app.user.full_cards[0].question == 'Test Question'

    @pytest.mark.integration
    @pytest.mark.database
    def test_card_data_persistence(self, app, test_user, mock_supabase):
        """Test that card data persists correctly"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Add a new card
        card = Card()
        full_card = FullCard(card, "Persistence Test", "Data saved correctly", ["persistence", "test"])
        test_user.full_cards.append(full_card)
        
        # Save user
        app.save_user()
        
        # Verify update was called
        mock_supabase.table.return_value.update.assert_called_once()
        
        # Get the saved data
        saved_data = mock_supabase.table.return_value.update.call_args[0][0]
        
        # Verify card data was saved correctly
        assert 'full_cards' in saved_data
        assert len(saved_data['full_cards']) == len(test_user.full_cards)
        
        # Find the persistence test card
        persistence_card = None
        for saved_card in saved_data['full_cards']:
            if saved_card['question'] == "Persistence Test":
                persistence_card = saved_card
                break
        
        assert persistence_card is not None
        assert persistence_card['answer'] == "Data saved correctly"
        assert "persistence" in persistence_card['tags']
        assert "test" in persistence_card['tags']

    @pytest.mark.integration
    @pytest.mark.database
    def test_review_log_persistence(self, app, test_user, mock_supabase):
        """Test that review logs persist correctly"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Create a card and review it
        card = Card()
        full_card = FullCard(card, "Review Test", "Test Answer", ["review"])
        test_user.full_cards.append(full_card)
        
        # Simulate review
        updated_card, review_log = test_user.scheduler.review_card(card, Rating.Good)
        full_card.card = updated_card
        test_user.review_logs.append(review_log)
        
        # Save user
        app.save_user()
        
        # Verify review log was saved
        saved_data = mock_supabase.table.return_value.update.call_args[0][0]
        assert 'review_logs' in saved_data
        assert len(saved_data['review_logs']) == len(test_user.review_logs)
        
        # Check review log data
        saved_log = saved_data['review_logs'][-1]  # Last review log
        assert saved_log['rating'] == Rating.Good
        assert 'review_time' in saved_log

    @pytest.mark.integration
    @pytest.mark.database
    def test_scheduler_state_persistence(self, app, test_user, mock_supabase):
        """Test that scheduler state persists correctly"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Modify scheduler settings (if applicable)
        # For now, just verify the scheduler is saved
        
        # Save user
        app.save_user()
        
        # Verify scheduler was saved
        saved_data = mock_supabase.table.return_value.update.call_args[0][0]
        assert 'scheduler' in saved_data
        
        # Verify scheduler data structure
        scheduler_data = saved_data['scheduler']
        assert isinstance(scheduler_data, dict)

    @pytest.mark.integration
    @pytest.mark.database
    def test_large_dataset_handling(self, app, mock_supabase):
        """Test handling of large datasets"""
        app.supabase = mock_supabase
        
        # Create a user with many cards
        user = User("Test User", "test@example.com", [], [], Scheduler())
        
        # Add many cards
        for i in range(100):
            card = Card()
            full_card = FullCard(card, f"Question {i}", f"Answer {i}", [f"tag{i % 10}"])
            user.full_cards.append(full_card)
        
        # Add many review logs
        for i in range(50):
            card = Card()
            updated_card, review_log = user.scheduler.review_card(card, Rating.Good)
            user.review_logs.append(review_log)
        
        app.user = user
        
        # Test saving large dataset
        app.save_user()
        
        # Verify save was called
        mock_supabase.table.return_value.update.assert_called_once()
        
        # Verify data integrity
        saved_data = mock_supabase.table.return_value.update.call_args[0][0]
        assert len(saved_data['full_cards']) == 100
        assert len(saved_data['review_logs']) == 50

    @pytest.mark.integration
    @pytest.mark.database
    def test_database_error_handling(self, app, test_user, mock_supabase):
        """Test database error handling"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Mock database error
        mock_supabase.table.return_value.update.side_effect = Exception("Database error")
        
        # Test that error is raised
        with pytest.raises(Exception):
            app.save_user()

    @pytest.mark.integration
    @pytest.mark.database
    def test_concurrent_user_operations(self, app, test_env, mock_supabase):
        """Test concurrent user operations"""
        app.supabase = mock_supabase
        
        # Simulate two users with same email (should not happen but test error handling)
        user1_data = {
            'id': 1,
            'name': 'User 1',
            'email': test_env['email'],
            'full_cards': [],
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }
        
        user2_data = {
            'id': 2,
            'name': 'User 2',
            'email': test_env['email'],
            'full_cards': [],
            'review_logs': [],
            'scheduler': Scheduler().to_dict()
        }
        
        # Mock database returning multiple users (should not happen)
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[user1_data, user2_data])
        
        # Test login - should handle first user
        app.login_or_signup(test_env['email'], test_env['password'])
        
        # Verify first user was loaded
        assert app.user is not None
        assert app.user.name == 'User 1'

    @pytest.mark.integration
    @pytest.mark.database
    def test_data_migration_compatibility(self, app, mock_supabase):
        """Test compatibility with different data formats (simulating migration)"""
        app.supabase = mock_supabase
        
        # Mock old data format (simulating migration scenario)
        old_format_data = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'full_cards': [],  # Empty cards
            'review_logs': [],  # Empty logs
            'scheduler': {}  # Empty scheduler (old format)
        }
        
        mock_supabase.table.return_value.execute.return_value = MagicMock(data=[old_format_data])
        
        # Test login with old format data
        try:
            app.login_or_signup('test@example.com', 'password')
            # Should handle gracefully or provide appropriate migration
            assert app.user is not None
        except Exception as e:
            # If it fails, it should be a specific migration error
            assert "migration" in str(e).lower() or "format" in str(e).lower()

    @pytest.mark.integration
    @pytest.mark.database
    def test_card_relationship_integrity(self, app, test_user, mock_supabase):
        """Test that card relationships are maintained correctly"""
        app.supabase = mock_supabase
        app.user = test_user
        
        # Create cards with relationships (tags)
        card1 = FullCard(Card(), "Question 1", "Answer 1", ["shared", "unique1"])
        card2 = FullCard(Card(), "Question 2", "Answer 2", ["shared", "unique2"])
        card3 = FullCard(Card(), "Question 3", "Answer 3", ["unique3"])
        
        test_user.full_cards.extend([card1, card2, card3])
        
        # Save user
        app.save_user()
        
        # Verify relationships are maintained
        saved_data = mock_supabase.table.return_value.update.call_args[0][0]
        
        # Check that shared tags are preserved
        shared_tag_count = 0
        for saved_card in saved_data['full_cards']:
            if "shared" in saved_card['tags']:
                shared_tag_count += 1
        
        assert shared_tag_count == 2  # Two cards should have the shared tag
        
        # Check unique tags
        unique_tags = set()
        for saved_card in saved_data['full_cards']:
            for tag in saved_card['tags']:
                if tag.startswith('unique'):
                    unique_tags.add(tag)
        
        assert len(unique_tags) == 3  # Should have unique1, unique2, unique3 