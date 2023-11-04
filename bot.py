import asyncio
import logging

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, Config
from tgbot.db.db import wait_postgres, close_db
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin.command import register_admin
from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.command import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    """
        Функция для регистрации всех Middleware. 
        Импортировать, после чего подключить по примеру, передав конфиг
    """
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp: Dispatcher):
    """
        Регистрация всех фильтров по примеру
    """
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    """
        Регистрация всех хендреров сообщений
    """
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def connection_db(config: Config):
    """
        Функция контроля подключения к базе данных
    """
    logger.info("Database connection. Wait for Postgres Database...")
    try:
        await wait_postgres(config=config)
    except tenacity.RetryError:
        logger.error("Failed to establish connection with Postgres Database.")
        exit(1)
    logger.info("Ready. Successful database connection.")


async def main():
    """
        Главная функция по запуску бота
    """

    # Делаем настройку вывода логирования
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    #Подгружаем конфиг
    config = load_config(".env")

    #Используем Redis если это необходимо
    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    #Засовываем конфиг в переменную бота
    bot['config'] = config

    #Если используется БД то идет подключение к ней
    if config.tg_bot.use_db:
        await connection_db(config=config)

    #Регистрация элементов
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    #Установление всех базовых комманд
    await set_default_commands(dp)

    #Оповещение всех админов
    for admin_id in config.tg_bot.admin_ids:
        await dp.bot.send_message(admin_id, "Бот запущен!")

    # start
    try:
        await dp.start_polling()
    finally:
        if config.tg_bot.use_db:
            await close_db()
        
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close() # type: ignore


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
