from sqlalchemy import Column, BigInteger, String, sql, Boolean

from tgbot.db.db import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    fullname = Column(String(100))

    query: sql.Select
