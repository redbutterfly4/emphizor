from fsrs import Scheduler, Card, ReviewLog
import json
from supabase import create_client, Client
import os


class FullCard:
    card: Card
    question: str
    answer: str
    tags: list[str]
    
    def __init__(self, card: Card, question: str, answer: str, tags: list[str]):
        self.card = card
        self.question = question
        self.answer = answer
        self.tags = tags
    
    def to_dict(self):
        return {
            "card": self.card.to_dict(),
            "question": self.question,
            "answer": self.answer,
            "tags": self.tags,
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
        supabase_url = "https://umtsnjvesqdhejjyexmg.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVtdHNuanZlc3FkaGVqanlleG1nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyNzcwNDMsImV4cCI6MjA2Njg1MzA0M30.q63otEn3JUIq5_G6t9gZlTi2tsBdcBNcs0L2Jtt8Mr4"
        # public key
        self.supabase = create_client(supabase_url, supabase_key)
        self.user = None

    def login_or_signup(self, email: str, password: str, name: str | None = None):
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            print(f"Login successful for {email}")
            # Login successful, try to get user from database
            try:
                self.user = self._get_user_from_db(email)
                print("User found in database")
            except ValueError:
                # Auth user exists but not in users table, create it
                print("User not found in database, creating user record")
                if name and name.strip():
                    scheduler = Scheduler()
                    new_user = User(name.strip(), email, [], [], scheduler)
                    self._create_user_in_db(new_user)
                    self.user = new_user
                    print("User record created successfully")
                else:
                    raise ValueError("User record missing. Name required to create user profile.")
        except Exception as login_error:
            print(f"Login failed: {login_error}")
            # Login failed, check if user exists in database first
            try:
                existing_user = self._get_user_from_db(email)
                print("User exists in database but login failed")
                raise ValueError("Login failed: Invalid credentials")
            except ValueError as db_error:
                print("User not found in database, attempting signup")
                # User doesn't exist, try to create new account
                if name and name.strip():
                    try:
                        self.supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })
                        print("Signup successful")
                        scheduler = Scheduler()
                        new_user = User(name.strip(), email, [], [], scheduler)
                        self._create_user_in_db(new_user)
                        self.user = new_user
                        print("New user created successfully")
                    except Exception as signup_error:
                        raise ValueError(f"Signup failed: {signup_error}")
                else:
                    raise ValueError("Name required for new user registration")

    def _get_user_from_db(self, email: str) -> User:
        response = self.supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            data = response.data[0]
            full_cards = [self._dict_to_full_card(card_dict) for card_dict in data["full_cards"]]
            review_logs = [ReviewLog.from_dict(log_dict) for log_dict in data["review_logs"]]
            scheduler = Scheduler.from_dict(data["scheduler"])
            user = User(data["name"], data["email"], full_cards, review_logs, scheduler)
            user.id = data["id"]
            return user
        raise ValueError("User not found in database")

    def _create_user_in_db(self, user: User):
        self.supabase.table("users").insert({
            "name": user.name,
            "email": user.email,
            "full_cards": [card.to_dict() for card in user.full_cards],
            "review_logs": [log.to_dict() for log in user.review_logs],
            "scheduler": user.scheduler.to_dict(),
        }).execute()

    def _dict_to_full_card(self, card_dict: dict) -> FullCard:
        card = Card.from_dict(card_dict["card"])
        return FullCard(card, card_dict["question"], card_dict["answer"], card_dict["tags"])

    def save_user(self):
        if self.user:
            self.supabase.table("users").update({
                "name": self.user.name,
                "email": self.user.email,
                "full_cards": [card.to_dict() for card in self.user.full_cards],
                "review_logs": [log.to_dict() for log in self.user.review_logs],
                "scheduler": self.user.scheduler.to_dict(),
            }).eq("id", self.user.id).execute() 