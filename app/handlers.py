import os

import yt_dlp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

import app.keyboards as kb
import database.requests as rq
from .file_name_collector import FilenameCollectorPP

router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username if user.username else "Не указано"
    await rq.set_user(user_id, username)
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=await kb.start_commands())


@router.callback_query(F.data == 'Скачать трек')
async def download_music(callback: CallbackQuery):
    await callback.answer('Скачать трек')
    await callback.message.answer('Какой трек вам нужен?')


async def download_music(arg):
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    filename_collector = FilenameCollectorPP()

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.add_post_processor(filename_collector)
            video_info = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]

        if filename_collector.filenames:
            file_path = filename_collector.filenames[0]
            return file_path
        else:
            return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


@router.message(F.text)
async def send_file(message: types.Message):
    arg = message.text.strip().split(' ', 1)
    if len(arg) < 2:
        await message.reply("Пожалуйста, укажите название трека.")
        return

    track_name = arg[1]

    file_path = await download_music(track_name)

    if file_path and os.path.exists(file_path):

        audio_file = FSInputFile(file_path)

        await message.reply_document(audio_file, caption=f"Вот ваш файл: {track_name}")

        os.remove(file_path)
    else:
        await message.reply("Не удалось найти или скачать трек.")
