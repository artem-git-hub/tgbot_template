"""
    Файл обработки комманд от всех администраторов
"""
import logging

from aiogram import Dispatcher
from aiogram.types import Message

logger = logging.getLogger(__name__)


async def admin_start(message: Message):
    """
        Комманда /start от админов
    """
    logger.info("me a first message") # Пример логирования
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    """
        Функция регистрации хендлеров и прикрипления этих хендлеров к конкретным функциям
    """
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
