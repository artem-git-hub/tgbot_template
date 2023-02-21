import asyncio
import logging

import tenacity
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.db.db import db
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin.command import register_admin
from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.command import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def wait_postgres(config):
    postgres_url = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
    await db.set_bind(postgres_url)
    if config.db.debug:
        await db.gino.drop_all()
        await db.gino.create_all()
    version = await db.scalar("SELECT version();")
    logger.info("Connected to {postgres}".format(postgres=version))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    logger.info("Database connection. Wait for Postgres Database...")
    try:
        await wait_postgres(config=config)
    except tenacity.RetryError:
        logger.error("Failed to establish connection with Postgres Database.")
        exit(1)
    logger.info("Ready. Successful database connection.")

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_default_commands(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
