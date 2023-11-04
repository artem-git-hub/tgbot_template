"""
    Файл с заданием middlewares (промежуточных точек контроля приходящих обновлений)
"""

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    """
        Какая-то промежуточная точка (хз зачем, но есть)
    """

    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, obj, data, *args):
        data.update(**self.kwargs)
