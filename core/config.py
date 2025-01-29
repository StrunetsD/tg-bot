import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = str(os.getenv('API_TOKEN'))
DATABASE_URL = str(os.getenv('DATABASE_URL'))
SPOTIFY_CLIENT_ID = str(os.getenv('SPOTIFY_CLIENT_ID')),
SPOTIFY_CLIENT_SECRET = str(os.getenv('SPOTIFY_CLIENT_SECRET')),
