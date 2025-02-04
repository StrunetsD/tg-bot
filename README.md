## About


Telegram bot that will give you the opportunity to
download your favorite tracks from spotify
## Docker
To use Docker with music_tg_bot, follow these steps:

1.Configurate .env file
```API_TOKEN=YOUR_API_TOKEN
ASYNC_DATABASE_URL=YOUR_ASYNC_DATABASE_URL
SYNC_DATABASE_URL=YOUR_SYNC_DATABASE_URL
DB_USER=user
DB_PASSWORD=passwoed
DB_NAME=db_name
DB_HOST=host
DB_PORT=db_port
SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
REDIS_URL= YOUR_REDIS_URL
SECRET_KEY=YOUR_SECRET_KEY
ADMIN_USERNAME=admin_username
ADMIN_PASSWORD=admin_password
```

2.Build the Docker images:

 ```sh
    docker-compose build
 ```
3.Run docker-compose:

 ```sh
    docker-compose up
 ```    

## Installation

If you prefer to run the bot without Docker, you can follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/StrunetsD/tg-bot.git
    cd tg-bot
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Linux/Mac
    .venv\Scripts\activate     # For Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure your `.env` file as described above.

5. Run the bot:

    ```bash
    python music_bot/run.py
    ```
## Technologies

- **Aiogram**
- **SQLAlchemy**
- **PostgreSQL**
- **Redis**
- **SpotifyAPI**
- **Flask**
- **Flask-admin**
- **Pytest**
- **HTML**
- **CSS**