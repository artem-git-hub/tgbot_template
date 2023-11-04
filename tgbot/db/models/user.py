"""
    Определение модели пользователя
"""

from sqlalchemy import Column, BigInteger, String, sql

from tgbot.db.db import TimedBaseModel


class User(TimedBaseModel):
    """
        Базовая модель пользователя
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    fullname = Column(String(100))

    query: sql.Select
