import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKS_PATH = BASE_DIR / 'tracks'

API_TOKEN = str(os.getenv('API_TOKEN'))
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID'),
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET'),
DATABASE_URL = str(os.getenv('DATABASE_URL'))
REDIS_URL=str(os.getenv('REDIS_URL'))
DB_CONNECTION = {
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT'],
    'dbname': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
}


