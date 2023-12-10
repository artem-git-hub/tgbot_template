"""
    Определение функций взаимодействия с базой данных для модели User
"""

from asyncpg import UniqueViolationError
from sqlalchemy import func

from tgbot.db.models.user import User


async def add_user(id_: int | str, username: str, fullname: str = ""):
    """Добавления пользователя [id_: str | int, username: str, fullname: str]"""
    try:
        id_ = int(id_) if isinstance(id_, str) else id_
        user = User(id=id_, username=username, fullname=fullname) # type: ignore

        await user.create() # type: ignore
    except UniqueViolationError:
        pass


async def select_all_users():
    """Выборка всех созданных пользователей"""

    users = await User.query.gino.all()
    return users


async def select_user(id_: int):
    """Выборка конкретного пользователя по его tg id [id_: str] """

    user = await User.query.where(User.id == id_).gino.first() # type: ignore
    return user


async def count_users():
    """Получение количества пользователей"""

    total = await func.count(User.id).gino.scalar()
    return total


async def update_user_data(id_: int, username: str = "", fullname: str = ""):
    """Обновление данных о пользоветеле по его tg id [id_: int, username: str, fullname: str]"""

    user = await User.get(id_)
    if username:
        await user.update(username=username).apply()
    if fullname:
        await user.update(fullname=fullname).apply()
        