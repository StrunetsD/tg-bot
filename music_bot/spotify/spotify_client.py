import os

from dotenv import load_dotenv
from core.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from .spotify import Spotify

load_dotenv()



spotify = Spotify(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)