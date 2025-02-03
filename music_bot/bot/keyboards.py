from aiogram.utils.keyboard import (InlineKeyboardBuilder, InlineKeyboardButton)
from music_bot.spotify.get_popular_tracks import search_playlist_tracks
from urllib.parse import quote

commands = ['Скачать трек']


async def start_commands():
    keyboard = InlineKeyboardBuilder()
    for comm in commands:
        keyboard.add(InlineKeyboardButton(text=comm, callback_data=comm))
    return keyboard.adjust(1).as_markup()


def truncate_track_name(track_name):
    return track_name[:64]

async def playlist_command():
    tracks = await search_playlist_tracks()
    keyboard = InlineKeyboardBuilder()

    if tracks:
        for track_name, track_artists, track_id in tracks:
            display_name = truncate_track_name(f"{track_name} by {track_artists}")
            safe_track_id = quote(track_id)
            print(f"Добавляем кнопку с callback_data: {safe_track_id}")

            if len(safe_track_id) > 64:
                print(f"Длина callback_data превышает 64 байта: {safe_track_id}")

            keyboard.add(InlineKeyboardButton(text=display_name, callback_data=safe_track_id))

    return keyboard.as_markup()