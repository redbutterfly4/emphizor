#!/usr/bin/env python3
"""
Improved comprehensive tests for Emphizor application
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
import json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.modules['fsrs'] = Mock()
sys.modules['supabase'] = Mock()
sys.modules['cryptography'] = Mock()
sys.modules['cryptography.fernet'] = Mock()
sys.modules['cryptography.hazmat'] = Mock()
sys.modules['cryptography.hazmat.primitives'] = Mock()
sys.modules['cryptography.hazmat.primitives.hashes'] = Mock()
sys.modules['cryptography.hazmat.primitives.kdf'] = Mock()
sys.modules['cryptography.hazmat.primitives.kdf.pbkdf2'] = Mock()

# Create improved mock classes that match the real interface
class MockCard:
    """Mock Card class that matches the fsrs Card interface"""
    def __init__(self, state="new", elapsed_days=0, difficulty=0.0, stability=0.0, retrievability=0.0, reps=0, lapses=0):
        self.state = state
        self.elapsed_days = elapsed_days
        self.difficulty = difficulty
        self.stability = stability
        self.retrievability = retrievability
        self.due = datetime.now()
        self.last_review = datetime.now()
        self.reps = reps
        self.lapses = lapses
    
    def to_dict(self):
        return {
            "state": self.state,
            "elapsed_days": self.elapsed_days,
            "difficulty": self.difficulty,
            "stability": self.stability,
            "retrievability": self.retrievability,
            "due": self.due.isoformat() if isinstance(self.due, datetime) else self.due,
            "last_review": self.last_review.isoformat() if isinstance(self.last_review, datetime) else self.last_review,
            "reps": self.reps,
            "lapses": self.lapses
        }
    
    @classmethod
    def from_dict(cls, data):
        card = cls()
        card.state = data.get("state", "new")
        card.elapsed_days = data.get("elapsed_days", 0)
        card.difficulty = data.get("difficulty", 0)
        card.stability = data.get("stability", 0)
        card.retrievability = data.get("retrievability", 0)
        card.reps = data.get("reps", 0)
        card.lapses = data.get("lapses", 0)
        # Handle datetime fields
        if "due" in data:
            card.due = datetime.fromisoformat(data["due"]) if isinstance(data["due"], str) else data["due"]
        if "last_review" in data:
            card.last_review = datetime.fromisoformat(data["last_review"]) if isinstance(data["last_review"], str) else data["last_review"]
        return card

class MockScheduler:
    """Mock Scheduler class that matches the fsrs Scheduler interface"""
    def __init__(self, parameters=None):
        self.parameters = parameters or {}
    
    def to_dict(self):
        return {"parameters": self.parameters}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data.get("parameters", {}))
    
    def schedule(self, card, rating):
        """Mock schedule method"""
        new_card = MockCard(
            state="learning" if rating >= 3 else "relearning",
            elapsed_days=card.elapsed_days + 1,
            difficulty=card.difficulty + (0.1 if rating < 3 else -0.1),
            stability=card.stability + 1,
            retrievability=max(0, card.retrievability - 0.1),
            reps=card.reps + 1,
            lapses=card.lapses + (1 if rating < 3 else 0)
        )
        return new_card

class MockReviewLog:
    """Mock ReviewLog class that matches the fsrs ReviewLog interface"""
    def __init__(self, rating=3, elapsed_days=0, review_time=None):
        self.rating = rating
        self.elapsed_days = elapsed_days
        self.review_time = review_time or datetime.now()
    
    def to_dict(self):
        return {
            "rating": self.rating,
            "elapsed_days": self.elapsed_days,
            "review_time": self.review_time.isoformat() if isinstance(self.review_time, datetime) else self.review_time
        }
    
    @classmethod
    def from_dict(cls, data):
        review_log = cls()
        review_log.rating = data.get("rating", 3)
        review_log.elapsed_days = data.get("elapsed_days", 0)
        if "review_time" in data:
            review_log.review_time = datetime.fromisoformat(data["review_time"]) if isinstance(data["review_time"], str) else data["review_time"]
        return review_log

# Set up mocks
sys.modules['fsrs'].Card = MockCard
sys.modules['fsrs'].Scheduler = MockScheduler
sys.modules['fsrs'].ReviewLog = MockReviewLog

# Mock supabase
mock_supabase = Mock()
sys.modules['supabase'].create_client = Mock(return_value=mock_supabase)

# Now import our modules
from base_classes import User, FullCard

class TestUserClass(unittest.TestCase):
    """Comprehensive tests for User class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scheduler = MockScheduler()
        User.id_generator = 0  # Reset ID generator for consistent tests
        
    def test_user_creation_basic(self):
        """Test creating a new user with basic attributes"""
        user = User("John Doe", "john@example.com", [], [], self.scheduler)
        
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(len(user.full_cards), 0)
        self.assertEqual(len(user.review_logs), 0)
        self.assertEqual(user.id, 1)
        self.assertIsInstance(user.scheduler, MockScheduler)
        print("✓ Basic user creation test passed")
    
    def test_user_id_generation(self):
        """Test that user IDs are generated sequentially"""
        user1 = User("User One", "user1@example.com", [], [], self.scheduler)
        user2 = User("User Two", "user2@example.com", [], [], self.scheduler)
        user3 = User("User Three", "user3@example.com", [], [], self.scheduler)
        
        self.assertEqual(user1.id, 1)
        self.assertEqual(user2.id, 2)
        self.assertEqual(user3.id, 3)
        print("✓ User ID generation test passed")
    
    def test_user_with_existing_cards(self):
        """Test creating a user with existing cards"""
        card1 = MockCard()
        card2 = MockCard(state="learning", elapsed_days=1)
        
        full_card1 = FullCard(card1, "Question 1", "Answer 1", {"tag1"})
        full_card2 = FullCard(card2, "Question 2", "Answer 2", {"tag2"})
        
        user = User("Test User", "test@example.com", [full_card1, full_card2], [], self.scheduler)
        
        self.assertEqual(len(user.full_cards), 2)
        self.assertEqual(user.full_cards[0].question, "Question 1")
        self.assertEqual(user.full_cards[1].question, "Question 2")
        print("✓ User with existing cards test passed")
    
    def test_user_with_review_logs(self):
        """Test creating a user with review logs"""
        review_log1 = MockReviewLog(rating=4, elapsed_days=1)
        review_log2 = MockReviewLog(rating=2, elapsed_days=3)
        
        user = User("Test User", "test@example.com", [], [review_log1, review_log2], self.scheduler)
        
        self.assertEqual(len(user.review_logs), 2)
        self.assertEqual(user.review_logs[0].rating, 4)
        self.assertEqual(user.review_logs[1].rating, 2)
        print("✓ User with review logs test passed")


class TestFullCardClass(unittest.TestCase):
    """Comprehensive tests for FullCard class"""
    
    def test_fullcard_creation_basic(self):
        """Test creating a flashcard with basic attributes"""
        card = MockCard()
        question = "What is the capital of France?"
        answer = "Paris"
        tags = {"geography", "capitals", "europe"}
        
        full_card = FullCard(card, question, answer, tags)
        
        self.assertEqual(full_card.question, question)
        self.assertEqual(full_card.answer, answer)
        self.assertEqual(full_card.tags, tags)
        self.assertIsInstance(full_card.card, MockCard)
        print("✓ Basic FullCard creation test passed")
    
    def test_fullcard_tags_are_set(self):
        """Test that tags are properly converted to a set"""
        card = MockCard()
        tags_list = ["python", "programming", "python", "coding"]  # duplicates
        
        full_card = FullCard(card, "Python question", "Python answer", set(tags_list))
        
        self.assertIsInstance(full_card.tags, set)
        self.assertEqual(full_card.tags, {"python", "programming", "coding"})
        print("✓ Tags conversion to set test passed")
    
    def test_fullcard_to_dict_basic(self):
        """Test converting FullCard to dictionary"""
        card = MockCard(state="new", elapsed_days=0)
        question = "What is 2 + 2?"
        answer = "4"
        tags = {"math", "basic", "arithmetic"}
        
        full_card = FullCard(card, question, answer, tags)
        card_dict = full_card.to_dict()
        
        self.assertEqual(card_dict["question"], question)
        self.assertEqual(card_dict["answer"], answer)
        self.assertEqual(set(card_dict["tags"]), tags)
        self.assertIn("card", card_dict)
        self.assertIsInstance(card_dict["card"], dict)
        self.assertEqual(card_dict["card"]["state"], "new")
        print("✓ FullCard to_dict test passed")
    
    def test_fullcard_to_dict_with_advanced_card(self):
        """Test to_dict with a more complex card state"""
        card = MockCard(
            state="learning",
            elapsed_days=5,
            difficulty=2.5,
            stability=10.0,
            retrievability=0.8
        )
        
        full_card = FullCard(card, "Complex question", "Complex answer", {"advanced"})
        card_dict = full_card.to_dict()
        
        self.assertEqual(card_dict["card"]["state"], "learning")
        self.assertEqual(card_dict["card"]["elapsed_days"], 5)
        self.assertEqual(card_dict["card"]["difficulty"], 2.5)
        self.assertEqual(card_dict["card"]["stability"], 10.0)
        self.assertEqual(card_dict["card"]["retrievability"], 0.8)
        print("✓ Advanced FullCard to_dict test passed")
    
    def test_fullcard_empty_tags(self):
        """Test FullCard with empty tags"""
        card = MockCard()
        full_card = FullCard(card, "Question", "Answer", set())
        
        self.assertEqual(full_card.tags, set())
        self.assertEqual(full_card.to_dict()["tags"], [])
        print("✓ Empty tags test passed")
    
    def test_fullcard_unicode_content(self):
        """Test FullCard with unicode content"""
        card = MockCard()
        question = "¿Cuál es la capital de España?"
        answer = "Madrid"
        tags = {"español", "geografía", "capitales"}
        
        full_card = FullCard(card, question, answer, tags)
        
        self.assertEqual(full_card.question, question)
        self.assertEqual(full_card.answer, answer)
        self.assertEqual(full_card.tags, tags)
        
        # Test serialization works with unicode
        card_dict = full_card.to_dict()
        self.assertEqual(card_dict["question"], question)
        self.assertEqual(card_dict["answer"], answer)
        print("✓ Unicode content test passed")


class TestMockClasses(unittest.TestCase):
    """Test that our mock classes work correctly"""
    
    def test_mock_card_serialization(self):
        """Test MockCard serialization and deserialization"""
        card = MockCard(state="learning", elapsed_days=3, difficulty=1.5)
        card_dict = card.to_dict()
        
        self.assertEqual(card_dict["state"], "learning")
        self.assertEqual(card_dict["elapsed_days"], 3)
        self.assertEqual(card_dict["difficulty"], 1.5)
        
        # Test deserialization
        new_card = MockCard.from_dict(card_dict)
        self.assertEqual(new_card.state, "learning")
        self.assertEqual(new_card.elapsed_days, 3)
        self.assertEqual(new_card.difficulty, 1.5)
        print("✓ MockCard serialization test passed")
    
    def test_mock_scheduler_functionality(self):
        """Test MockScheduler scheduling functionality"""
        scheduler = MockScheduler({"param1": "value1"})
        card = MockCard(state="new", elapsed_days=0, reps=0)
        
        # Test good rating
        new_card = scheduler.schedule(card, 4)
        self.assertEqual(new_card.state, "learning")
        self.assertEqual(new_card.reps, 1)
        self.assertEqual(new_card.lapses, 0)
        
        # Test bad rating
        bad_card = scheduler.schedule(card, 1)
        self.assertEqual(bad_card.state, "relearning")
        self.assertEqual(bad_card.lapses, 1)
        print("✓ MockScheduler functionality test passed")
    
    def test_mock_review_log_serialization(self):
        """Test MockReviewLog serialization"""
        review_log = MockReviewLog(rating=5, elapsed_days=2)
        log_dict = review_log.to_dict()
        
        self.assertEqual(log_dict["rating"], 5)
        self.assertEqual(log_dict["elapsed_days"], 2)
        
        # Test deserialization
        new_log = MockReviewLog.from_dict(log_dict)
        self.assertEqual(new_log.rating, 5)
        self.assertEqual(new_log.elapsed_days, 2)
        print("✓ MockReviewLog serialization test passed")


class TestAppIntegration(unittest.TestCase):
    """Integration tests for App class with mocked dependencies"""
    
    @patch('base_classes.create_client')
    def test_app_initialization(self, mock_create_client):
        """Test App initialization with mocked Supabase"""
        mock_supabase = Mock()
        mock_create_client.return_value = mock_supabase
        
        from base_classes import App
        
        app = App()
        self.assertIsNotNone(app.supabase)
        self.assertIsNone(app.user)
        mock_create_client.assert_called_once()
        print("✓ App initialization test passed")
    
    @patch('base_classes.create_client')
    def test_app_user_workflow(self, mock_create_client):
        """Test complete user workflow with app"""
        mock_supabase = Mock()
        mock_create_client.return_value = mock_supabase
        
        from base_classes import App
        
        app = App()
        
        # Create a user and assign to app
        scheduler = MockScheduler()
        user = User("Test User", "test@example.com", [], [], scheduler)
        
        # Add some cards to the user
        card1 = MockCard()
        card2 = MockCard(state="learning")
        full_card1 = FullCard(card1, "Question 1", "Answer 1", {"programming"})
        full_card2 = FullCard(card2, "Question 2", "Answer 2", {"math"})
        
        user.full_cards = [full_card1, full_card2]
        
        # Add review logs
        review_log = MockReviewLog(rating=4, elapsed_days=1)
        user.review_logs = [review_log]
        
        app.user = user
        
        # Test that everything is properly set up
        self.assertEqual(app.user.name, "Test User")
        self.assertEqual(len(app.user.full_cards), 2)
        self.assertEqual(len(app.user.review_logs), 1)
        self.assertEqual(app.user.full_cards[0].question, "Question 1")
        self.assertEqual(app.user.review_logs[0].rating, 4)
        print("✓ App user workflow test passed")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def test_empty_user_creation(self):
        """Test creating user with empty name and email"""
        scheduler = MockScheduler()
        user = User("", "", [], [], scheduler)
        
        self.assertEqual(user.name, "")
        self.assertEqual(user.email, "")
        self.assertIsInstance(user.id, int)
        self.assertTrue(user.id > 0)
        print("✓ Empty user creation test passed")
    
    def test_fullcard_with_very_long_content(self):
        """Test FullCard with very long question and answer"""
        card = MockCard()
        long_question = "What is " + "very " * 100 + "long question?"
        long_answer = "This is " + "very " * 100 + "long answer."
        
        full_card = FullCard(card, long_question, long_answer, {"test"})
        
        self.assertEqual(full_card.question, long_question)
        self.assertEqual(full_card.answer, long_answer)
        
        # Test serialization works with long content
        card_dict = full_card.to_dict()
        self.assertEqual(len(card_dict["question"]), len(long_question))
        self.assertEqual(len(card_dict["answer"]), len(long_answer))
        print("✓ Long content test passed")
    
    def test_many_tags(self):
        """Test FullCard with many tags"""
        card = MockCard()
        many_tags = {f"tag_{i}" for i in range(100)}
        
        full_card = FullCard(card, "Question", "Answer", many_tags)
        
        self.assertEqual(len(full_card.tags), 100)
        self.assertEqual(full_card.tags, many_tags)
        
        # Test serialization
        card_dict = full_card.to_dict()
        self.assertEqual(len(card_dict["tags"]), 100)
        self.assertEqual(set(card_dict["tags"]), many_tags)
        print("✓ Many tags test passed")


if __name__ == '__main__':
    print("Running comprehensive Emphizor tests...")
    print("=" * 60)
    
    # Run tests with detailed output
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes in order
    test_classes = [
        TestUserClass,
        TestFullCardClass,
        TestMockClasses,
        TestAppIntegration,
        TestEdgeCases
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("All tests passed successfully! ✅")
        print(f"Tests run: {result.testsRun}")
    else:
        print("Some tests failed! ❌")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}") 