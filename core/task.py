import asyncio
import os
import time

from .config import TRACKS_PATH


async def check_downloaded_track_ages():
    while True:
        for track in os.listdir(TRACKS_PATH):
            track_path = TRACKS_PATH / track
            track_age = time.time() - os.path.getatime(track_path)

            if track_age > 3600:
                os.remove(track_path)

        await asyncio.sleep(10)


async def run_tasks():
    asyncio.create_task(check_downloaded_track_ages())
