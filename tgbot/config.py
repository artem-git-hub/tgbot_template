"""
    Файл создания конфигурационных классов и загрузки из .env файла переменных окружения 
"""

from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DbConfig:
    """Класс для конфигурации базы данных"""

    host: str
    password: str
    user: str
    database: str
    debug: bool


@dataclass
class TgBot:
    """Класс конфигурации бота"""

    token: str
    admin_ids: List[int]
    use_redis: bool
    use_db: bool


@dataclass
class Miscellaneous:
    """Класс для других параметров (опционально), не заполняется"""

    other_params: str = ""


@dataclass
class Config:
    """Общий класс конфигурации"""

    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = ""):
    """
        Функция загрузки конфигурационных переменных в класс конфигурации
    """

    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            use_db=env.bool("USE_DB")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            debug=env.str('DEBUG')
        ),
        misc=Miscellaneous()
    )
