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
        User.id += 1
        self.id = User.id
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
