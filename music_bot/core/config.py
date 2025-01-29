import os
from pathlib import Path


from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKS_PATH = BASE_DIR / 'tracks'

API_TOKEN = str(os.getenv('API_TOKEN'))
SPOTIFY_CLIENT_ID = str(os.getenv('SPOTIFY_CLIENT_ID')),
SPOTIFY_CLIENT_SECRET = str(os.getenv('SPOTIFY_CLIENT_SECRET')),
DATABASE_URL = str(os.getenv('DATABASE_URL'))
