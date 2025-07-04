"""
Test configuration and fixtures for Emphizor integration tests.
"""

import pytest
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone
from unittest.mock import MagicMock

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_classes import App, User, FullCard
from fsrs import Card, Scheduler, Rating

# Load test environment variables
load_dotenv('test.env')

@pytest.fixture(scope="session")
def test_env():
    """Load test environment variables"""
    return {
        'email': os.getenv('TEST_USER_EMAIL', 'test@emphizor.com'),
        'password': os.getenv('TEST_USER_PASSWORD', 'testpassword123'),
        'name': os.getenv('TEST_USER_NAME', 'Test User'),
        'email_2': os.getenv('TEST_USER_2_EMAIL', 'test2@emphizor.com'),
        'password_2': os.getenv('TEST_USER_2_PASSWORD', 'testpassword456'),
        'name_2': os.getenv('TEST_USER_2_NAME', 'Test User 2'),
    }

@pytest.fixture(scope="function")
def app():
    """Create a fresh App instance for each test"""
    return App()

@pytest.fixture(scope="function")
def test_user():
    """Create a test user with some sample data"""
    scheduler = Scheduler()
    user = User("Test User", "test@emphizor.com", [], [], scheduler)
    
    # Add some sample cards
    card1 = Card()
    full_card1 = FullCard(card1, "What is Python?", "A programming language", ["programming", "python"])
    
    card2 = Card()
    full_card2 = FullCard(card2, "What is FSRS?", "A spaced repetition algorithm", ["learning", "algorithm"])
    
    user.full_cards = [full_card1, full_card2]
    
    return user

@pytest.fixture(scope="function")
def sample_cards():
    """Create sample cards for testing"""
    cards = []
    
    # Create different types of cards
    test_data = [
        ("What is 2+2?", "4", ["math", "basic"]),
        ("What is the capital of France?", "Paris", ["geography", "europe"]),
        ("What is the Python print function?", "print()", ["programming", "python"]),
        ("What year was Python created?", "1991", ["programming", "history"]),
        ("What is HTML?", "HyperText Markup Language", ["web", "programming"]),
    ]
    
    for question, answer, tags in test_data:
        card = Card()
        full_card = FullCard(card, question, answer, tags)
        cards.append(full_card)
    
    return cards

@pytest.fixture(scope="function")
def due_cards():
    """Create cards that are due for review"""
    cards = []
    past_time = datetime.now(timezone.utc)
    
    test_data = [
        ("Due question 1", "Due answer 1", ["tag1"]),
        ("Due question 2", "Due answer 2", ["tag2"]),
        ("Due question 3", "Due answer 3", ["tag3"]),
    ]
    
    for question, answer, tags in test_data:
        card = Card()
        card.due = past_time  # Set to past time to make it due
        full_card = FullCard(card, question, answer, tags)
        cards.append(full_card)
    
    return cards

@pytest.fixture(scope="function")
def mock_qt_application():
    """Mock Qt application for GUI tests"""
    from unittest.mock import MagicMock
    
    # Mock QApplication
    mock_app = MagicMock()
    mock_app.exec.return_value = 0
    
    # Mock QDialog
    mock_dialog = MagicMock()
    mock_dialog.exec.return_value = 1  # Accepted
    
    return {
        'app': mock_app,
        'dialog': mock_dialog
    }

@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Clean up test data after each test"""
    yield
    # Any cleanup code can go here if needed

@pytest.fixture(scope="function")
def authenticated_app(app, test_env):
    """Create an authenticated app instance"""
    # This fixture should be used carefully as it will make actual API calls
    # In a real test environment, you might want to mock the authentication
    app.user = None  # Reset user state
    return app

@pytest.fixture(scope="function")
def mock_supabase():
    """Mock Supabase client for testing without actual database calls"""
    from unittest.mock import MagicMock
    
    mock_client = MagicMock()
    mock_auth = MagicMock()
    mock_table = MagicMock()
    
    # Mock successful auth responses
    mock_auth.sign_in_with_password.return_value = MagicMock(
        user={'id': 'test-id', 'email': 'test@example.com'}
    )
    mock_auth.sign_up.return_value = MagicMock(
        user={'id': 'test-id', 'email': 'test@example.com'}
    )
    
    # Mock table operations
    mock_table.select.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.execute.return_value = MagicMock(data=[])
    
    mock_client.auth = mock_auth
    mock_client.table.return_value = mock_table
    
    return mock_client 