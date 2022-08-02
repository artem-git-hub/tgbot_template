from aiogram import Dispatcher, types

from tgbot.handlers.users.admin import admin_start
from tgbot.handlers.users.echo import bot_echo, bot_echo_all
from tgbot.handlers.users.user import user_start


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
