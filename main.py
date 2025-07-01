from fsrs import Scheduler, Card, Rating, ReviewLog
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

scheduler = Scheduler()

# note: all new cards are 'due' immediately upon creation
card = Card()

# Rating.Again (==1) forgot the card
# Rating.Hard (==2) remembered the card with serious difficulty
# Rating.Good (==3) remembered the card after a hesitation
# Rating.Easy (==4) remembered the card easily

rating = Rating.Good

card, review_log = scheduler.review_card(card, rating)

print(f"Card rated {review_log.rating} at {review_log.review_datetime}")
# > Card rated 3 at 2024-11-30 17:46:58.856497+00:00

from datetime import datetime, timezone

due = card.due

# how much time between when the card is due and now
time_delta = due - datetime.now(timezone.utc)

print(f"Card due on {due}")
print(f"Card due in {time_delta.seconds} seconds")

# > Card due on 2024-11-30 18:42:36.070712+00:00
# > Card due in 599 seconds

class FullCard:
    card: Card
    question: str
    answer: str
    tags: list[str]
    user: int
    
    def __init__(self, card: Card, question: str, answer: str, tags: list[str], user: int):
        self.card = card
        self.question = question
        self.answer = answer
        self.tags = tags
        self.user = user

full_card = FullCard(card, "What is the capital of France?", "Paris", ["матан", "линал"], 1)

# User = {
#     "id": 1,
#     "name": "John Doe",
#     "email": "john.doe@example.com",
#     "full_cards": [full_card],
#     "review_logs": [review_log],
#     "scheduler": scheduler,
#     "tags": ["матан", "линал"],
# }

class User:
    id: int
    name: str
    email: str
    full_cards: list[FullCard]
    review_logs: list[ReviewLog]
    scheduler: Scheduler
    tags: list[str]
    
    def __init__(self, id, name, email, full_cards, review_logs, scheduler, tags):
        self.id = id
        self.name = name
        self.email = email
        self.full_cards = full_cards
        self.review_logs = review_logs
        self.scheduler = scheduler
        self.tags = tags

user = User(1, "John Doe", "john.doe@example.com", [full_card], [review_log], scheduler, ["матан", "линал"])
print(user.id)
print(user.name)
print(user.email)
print(user.full_cards[0].question)
print(user.scheduler.to_dict())
print(user.tags)

url = os.environ.get("SUPABASE_URL") or ''
key = os.environ.get("SUPABASE_KEY") or ''
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(url, key)
# response = (
#     supabase.table("users")
#     .select("*")
#     .execute()
# )