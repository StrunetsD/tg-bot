from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def test(message: Message):
    await message.reply('FSDFSF', reply_markup=kb.main)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello")



