import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = str(os.getenv('TOKEN'))
DATABASE_URL = str(os.getenv('DATABASE_URL'))
