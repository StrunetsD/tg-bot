from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder,
                                    InlineKeyboardMarkup, InlineKeyboardButton)


# main = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Добавить песню', callback_data='add_music'),
#             InlineKeyboardButton(text='Создать плейлист', callback_data='add_playlist'),
#             InlineKeyboardButton(text='Добавить песню в плейлист', callback_data='add_music_to_playlist'),
#             InlineKeyboardButton(text='Новинки', callback_data='new'),
#             InlineKeyboardButton(text='Популярное', callback_data='popular'),
#         ]
#     ],
# )

commands = ['Скачать трек','Создать плейлист','Добавить трек в плейлист','Новинки', 'Популярное']

async def start_commands():
    keyboard = InlineKeyboardBuilder()
    for comm in commands:
        keyboard.add(InlineKeyboardButton(text=comm, callback_data=comm))
    return keyboard.adjust(1).as_markup()