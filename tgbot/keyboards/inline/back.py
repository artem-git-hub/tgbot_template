"""
    Пример создания клавиатуры
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_data import for_key_back


async def def_key_back():
    """
        Функция возвращающая клавиатуру
    """

    key_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Назад',
                    callback_data=for_key_back.new(command="back")
                ), # type: ignore
            ]
        ]
    )
    return key_back
