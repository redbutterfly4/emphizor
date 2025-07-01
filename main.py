from fsrs import Scheduler, Card, Rating, ReviewLog
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

# Import our custom classes
from models import FullCard, User

load_dotenv()

scheduler = Scheduler()

card = Card()

# Rating.Again (==1) forgot the card
# Rating.Hard (==2) remembered the card with serious difficulty
# Rating.Good (==3) remembered the card after a hesitation
# Rating.Easy (==4) remembered the card easily

rating = Rating.Again

card, review_log = scheduler.review_card(card, rating)

print(f"Card rated {review_log.rating} at {review_log.review_datetime}")
# > Card rated 3 at 2024-11-30 17:46:58.856497+00:00

due = card.due

# how much time between when the card is due and now
time_delta = due - datetime.now(timezone.utc)

print(f"Card due on {due}")
print(f"Card due in {time_delta.seconds} seconds")

# > Card due on 2024-11-30 18:42:36.070712+00:00
# > Card due in 599 seconds

full_card = FullCard(card, "What is python?", "Python is a programming language", ["programming"])

user = User(1, "John Doe", "john.doe@example.com", [full_card], [review_log], scheduler)
print(user.id)
print(user.name)
print(user.email)
print(user.full_cards[0].question)
print(user.scheduler.to_dict())

url = os.environ.get("SUPABASE_URL") or ''
key = os.environ.get("SUPABASE_KEY") or ''
if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(url, key)




# response = (
#     supabase.table("users")
#     .insert({
#         "name": user.name, 
#         "email": user.email, 
#         "full_cards": [card.to_dict() for card in user.full_cards], 
#         "review_logs": [log.to_dict() for log in user.review_logs], 
#         "scheduler": user.scheduler.to_dict(), 
#         "tags": user.tags
#     })
#     .execute()
# )

# user.save_to_supabase(supabase)
response = (
    supabase.table("users")
    .select("*")
    .execute()
)