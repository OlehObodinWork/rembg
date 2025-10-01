import os
from dotenv import load_dotenv

load_dotenv()
BACKBLAZE_KEY_ID = os.getenv("BACKBLAZE_KEY_ID")
BACKBLAZE_KEY = os.getenv("BACKBLAZE_KEY")
BACKBLAZE_BUCKET_ID = os.getenv("BACKBLAZE_BUCKET_ID")
BACKBLAZE_API_AUTH_URL = "https://api.backblazeb2.com/b2api/v4/b2_authorize_account"

if not all([BACKBLAZE_KEY_ID, BACKBLAZE_KEY, BACKBLAZE_BUCKET_ID, BACKBLAZE_API_AUTH_URL]):
    raise EnvironmentError("Missing Backblaze credentials in environment variables")

