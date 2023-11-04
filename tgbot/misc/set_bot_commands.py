"""
    Файл для установки комманд бота
"""

from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    """Функция установки комманд бота"""

    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Стартуем или перезапускаемся")
        ]
    )
