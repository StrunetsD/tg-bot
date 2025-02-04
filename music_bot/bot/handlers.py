import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Chat, Message
from spotipy.exceptions import SpotifyException

from core.config import REDIS_URL, API_TOKEN
from database import db_requests as rq
from database.models import UserRole
from music_bot.middleware.throttling_middleware import ThrottlingMiddleware
from music_bot.spotify import download
from music_bot.spotify.spotify_client import spotify
from . import keyboards as kb

storage = RedisStorage.from_url(REDIS_URL)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)
dp.message.middleware.register(ThrottlingMiddleware(storage=storage))


@dp.message(Command("start"))
async def send_welcome(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username if user.username else "Не указано"
    await rq.set_user(user_id, username)
    await message.answer(
        text="Выберите действие:",
        reply_markup=await kb.start_commands()
    )


@dp.callback_query(F.data == 'Скачать трек')
async def download_music(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer('Скачать трек')
    await callback.message.answer('Какой трек вам нужен?')
    await storage.redis.set(f"waiting_for_track:{user_id}", "true")


@dp.message(F.text)
async def message_handler(message: Message, event_chat: Chat):
    user_id = message.from_user.id
    try:
        user_role = await rq.get_user_role(user_id)
    except ValueError:
        await message.reply("Пользователь не найден.")
        return

    if user_role == UserRole.block:
        await message.reply("Вы заблокированы и не можете отправлять сообщения.")
        return
    waiting_state = await storage.redis.get(f"waiting_for_track:{user_id}")

    if waiting_state is None:
        await message.answer(
            text="Треки:",
            reply_markup=await kb.start_commands()
        )
        return

    if not message.text:
        await message.reply(text='Пожалуйста, отправьте название трека')
        return
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
            user_id=user_id,
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
            download.download_and_send_song(
                bot=bot,
                chat=event_chat,
                message=message,
                song=song
            )
            for song in songs
        ]
    )
    await rq.add_user_query(
        user_id=user_id,
        username=message.from_user.username,
        query=message.text
    )
    await storage.redis.delete(f"waiting_for_track:{user_id}")
