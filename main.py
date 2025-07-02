from fsrs import Scheduler, Card, Rating, ReviewLog
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

from models import FullCard, User

load_dotenv()

url = os.environ.get("SUPABASE_URL") or ''
key = os.environ.get("SUPABASE_KEY") or ''
email = os.environ.get("USER_EMAIL") or ''
password = os.environ.get("USER_PASSWORD") or ''
if not url or not key or not email or not password:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY and USER_EMAIL and USER_PASSWORD must be set")

supabase: Client = create_client(url, key)

# response = supabase.auth.sign_up({
#     "email": email,
#     "password": password
# })

response = supabase.auth.sign_up_with_oauth(
    {"provider": "github"}
)