"""
    Определение ответов на комманды от пользователей
"""

from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message):
    """Ответ на комманду /start"""

    await message.reply("Hello, users!")


def register_user(dp: Dispatcher):
    """Регистрация хендлеров"""

    dp.register_message_handler(user_start, commands=["start"], state="*")
