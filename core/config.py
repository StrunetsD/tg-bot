import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKS_PATH = BASE_DIR / 'tracks'

API_TOKEN = str(os.getenv('API_TOKEN'))
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID'),
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET'),
ASYNC_DATABASE_URL = str(os.getenv('ASYNC_DATABASE_URL'))
SYNC_DATABASE_URL = str(os.getenv('SYNC_DATABASE_URL'))
REDIS_URL = str(os.getenv('REDIS_URL'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))
ADMIN_PASSWORD = str(os.getenv('ADMIN_PASSWORD'))
ADMIN_USERNAME = str(os.getenv('ADMIN_USERNAME'))
