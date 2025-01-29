import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Chat, Message
from spotipy.exceptions import SpotifyException

import bot.keyboards as kb
import database.requests as rq
from core.config import API_TOKEN
from spotify.spotify_client import spotify
from .download import download_and_send_song

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def send_welcome(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username if user.username else "Не указано"
    await rq.set_user(user_id, username)
    await message.answer(
        text="Добро пожаловать! Выберите действие:",
        reply_markup=await kb.start_commands()
    )


@dp.callback_query(F.data == 'Скачать трек')
async def download_music(callback: CallbackQuery):
    await callback.answer('Скачать трек')
    await callback.message.answer('Какой трек вам нужен?')


@dp.message(F.text)
async def message_handler(message: Message, event_chat: Chat):
    if not message.text:
        await message.reply(
            text='Пожалуйста, отправьте название трека'
        )

    await rq.add_user_query(
        user_id=message.from_user.id,
        username=message.from_user.username,
        query=message.text
    )

    await bot.send_chat_action(
        chat_id=event_chat.id,
        action=ChatAction.RECORD_VOICE
    )

    try:
        songs = await spotify.search([message.text])
    except SpotifyException:
        await message.reply(
            text='Не найдено'
        )
        await rq.add_failed_user_query(
            user_id=message.from_user.id,
            username=message.from_user.username,
            query=message.text
        )
        return

    await bot.send_chat_action(
        chat_id=event_chat.id,
        action=ChatAction.RECORD_VOICE
    )

    await asyncio.gather(
        *[
            download_and_send_song(
                bot=bot,
                chat=event_chat,
                message=message,
                song=song
            )
            for song in songs
        ]
    )
