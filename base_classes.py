from fsrs import Scheduler, Card, ReviewLog
import json
from supabase import create_client, Client
import os
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)


class FullCard:
    card: Card
    question: str
    answer: str
    tags: set
    
    def __init__(self, card: Card, question: str, answer: str, tags: set):
        self.card = card
        self.question = question
        self.answer = answer
        self.tags = set(tags)
    
    def to_dict(self):
        return {
            "card": self.card.to_dict(),
            "question": self.question,
            "answer": self.answer,
            "tags": sorted(list(self.tags)),
        }


class User:
    id_generator = 0 # static variable for id
    id: int
    name: str
    email: str
    full_cards: list[FullCard]
    review_logs: list[ReviewLog]
    scheduler: Scheduler
    
    def __init__(self, name, email, full_cards, review_logs, scheduler):
        User.id_generator += 1
        self.id = User.id_generator
        self.name = name
        self.email = email
        self.full_cards = full_cards
        self.review_logs = review_logs
        self.scheduler = scheduler
        logger.info(f"Created new User: {name} ({email}) with {len(full_cards)} cards")

    def save_to_supabase(self, supabase: Client):
        response = supabase.table("users").insert({
            "name": self.name,
            "email": self.email,
            "full_cards": [card.to_dict() for card in self.full_cards],
            "review_logs": [log.to_dict() for log in self.review_logs],
            "scheduler": self.scheduler.to_dict(),
        }).execute()
        print(response) 


class App:
    def __init__(self):
        logger.info("Initializing App with Supabase connection")
        supabase_url = "https://umtsnjvesqdhejjyexmg.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVtdHNuanZlc3FkaGVqanlleG1nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyNzcwNDMsImV4cCI6MjA2Njg1MzA0M30.q63otEn3JUIq5_G6t9gZlTi2tsBdcBNcs0L2Jtt8Mr4"
        # public key
        self.supabase = create_client(supabase_url, supabase_key)
        self.user = None
        logger.info("App initialized successfully with Supabase client")

    def login_or_signup(self, email: str, password: str, name: str | None = None):
        logger.info(f"Attempting login/signup for email: {email}")
        try:
            logger.debug("Attempting Supabase authentication login")
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            logger.info(f"Login successful for {email}")
            # Login successful, try to get user from database
            try:
                logger.debug("Attempting to get user from database")
                self.user = self._get_user_from_db(email)
                logger.info("User found in database and loaded successfully")
            except ValueError:
                # Auth user exists but not in users table, create it
                logger.warning("User not found in database, creating user record")
                if name and name.strip():
                    scheduler = Scheduler()
                    new_user = User(name.strip(), email, [], [], scheduler)
                    self._create_user_in_db(new_user)
                    self.user = new_user
                    logger.info("User record created successfully")
                else:
                    logger.error("User record missing and no name provided")
                    raise ValueError("User record missing. Name required to create user profile.")
        except Exception as login_error:
            logger.warning(f"Login failed: {login_error}")
            # Login failed, check if user exists in database first
            try:
                existing_user = self._get_user_from_db(email)
                logger.error("User exists in database but login failed")
                raise ValueError("Login failed: Invalid credentials")
            except ValueError as db_error:
                logger.info("User not found in database, attempting signup")
                # User doesn't exist, try to create new account
                if name and name.strip():
                    try:
                        logger.debug("Attempting Supabase authentication signup")
                        self.supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })
                        logger.info("Signup successful")
                        scheduler = Scheduler()
                        new_user = User(name.strip(), email, [], [], scheduler)
                        self._create_user_in_db(new_user)
                        self.user = new_user
                        logger.info("New user created successfully")
                    except Exception as signup_error:
                        logger.error(f"Signup failed: {signup_error}", exc_info=True)
                        raise ValueError(f"Signup failed: {signup_error}")
                else:
                    logger.error("Name required for new user registration")
                    raise ValueError("Name required for new user registration")

    def _get_user_from_db(self, email: str) -> User:
        logger.info(f"Fetching user from database: {email}")
        response = self.supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            data = response.data[0]
            logger.debug(f"User data found in database with {len(data.get('full_cards', []))} cards")
            full_cards = [self._dict_to_full_card(card_dict) for card_dict in data["full_cards"]]
            review_logs = [ReviewLog.from_dict(log_dict) for log_dict in data["review_logs"]]
            scheduler = Scheduler.from_dict(data["scheduler"])
            user = User(data["name"], data["email"], full_cards, review_logs, scheduler)
            user.id = data["id"]
            logger.info(f"User loaded from database: {user.name} with {len(full_cards)} cards")
            return user
        logger.warning(f"User not found in database: {email}")
        raise ValueError("User not found in database")

    def _create_user_in_db(self, user: User):
        logger.info(f"Creating new user in database: {user.name} ({user.email})")
        try:
            self.supabase.table("users").insert({
                "name": user.name,
                "email": user.email,
                "full_cards": [card.to_dict() for card in user.full_cards],
                "review_logs": [log.to_dict() for log in user.review_logs],
                "scheduler": user.scheduler.to_dict(),
            }).execute()
            logger.info(f"User created successfully in database: {user.email}")
        except Exception as e:
            logger.error(f"Failed to create user in database: {str(e)}", exc_info=True)
            raise

    def _dict_to_full_card(self, card_dict: dict) -> FullCard:
        card = Card.from_dict(card_dict["card"])
        return FullCard(card, card_dict["question"], card_dict["answer"], card_dict["tags"])

    def save_user(self):
        if self.user:
            logger.info(f"Saving user data for: {self.user.email}")
            logger.debug(f"Saving {len(self.user.full_cards)} cards and {len(self.user.review_logs)} review logs")
            try:
                self.supabase.table("users").update({
                    "name": self.user.name,
                    "email": self.user.email,
                    "full_cards": [card.to_dict() for card in self.user.full_cards],
                    "review_logs": [log.to_dict() for log in self.user.review_logs],
                    "scheduler": self.user.scheduler.to_dict(),
                }).eq("id", self.user.id).execute()
                logger.info("User data saved successfully to database")
            except Exception as e:
                logger.error(f"Failed to save user data: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning("Attempted to save user but no user is logged in") 