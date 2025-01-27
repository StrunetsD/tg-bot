from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardMarkup, InlineKeyboardButton)


commands = ['Скачать трек','Плейлист','Создать плейлист','Добавить трек в плейлист','Новинки', 'Популярное']

async def start_commands():
    keyboard = InlineKeyboardBuilder()
    for comm in commands:
        keyboard.add(InlineKeyboardButton(text=comm, callback_data=comm))
    return keyboard.adjust(1).as_markup()