"""
    Основной файл для создания, подключения и отправки запросов к базе данных 
"""
import logging
from typing import List

from gino import Gino
import sqlalchemy
from sqlalchemy import Column, DateTime, func

from tgbot.config import Config

logger = logging.getLogger(__name__)
db = Gino()


class BaseModel(db.Model):
    """
        Базовая модель базы данных на которой основываются остальные.
        Здесь задается вывод каждой модели
    """
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table = sqlalchemy.inspect(self.__class__) # type of: sqlalchemy.Table
        primary_key_columns: List[sqlalchemy.Column] = table.primary_key.columns # type: ignore
        values = {
            column.name: getattr(self, self.column_name_map[column.name]) # type: ignore
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    """
        Абстрактная модель которая содержит два столбца: время создания и последнего изменения
    """
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(
        DateTime(True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )


async def wait_postgres(config: Config):
    """
        Функция подключения к базе данных
    """
    postgres_url = f"""
                        postgresql://{config.db.user}:{config.db.password}
                        @{config.db.host}/{config.db.database}"""
    await db.set_bind(postgres_url)

    if config.db.debug:
        await db.gino.drop_all()
        await db.gino.create_all()

    version = await db.scalar("SELECT version();")
    logger.info("Connected to %s", version)

async def close_db():
    """
        Функция отключения от базы данных и закрытия соединения
    """
    bind = db.pop_bind()
    if bind:
        logger.info("Close PostgreSQL Connection")
        await bind.close()
