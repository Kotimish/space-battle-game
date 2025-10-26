from concurrent.futures import Future

from src.dependencies.ioc import IoC
from src.interfaces.base_command import BaseCommand
from src.interfaces.uobject import UObject


class GetAllObjectsCommand(BaseCommand):
    """Команда получения информации о состоянии игровой сессии"""
    def __init__(self, future: Future):
        self.future = future

    def execute(self) -> None:
        try:
            # Получение из скоупа текущей сессии словарь игровых объектов
            game_objects = IoC[dict[str, UObject]].resolve('Game.Object.GetAll')
            state = {
                object_id: uobject.to_dict()
                for object_id, uobject in game_objects.items()
            }
            self.future.set_result(state)
        except Exception as e:
            self.future.set_exception(e)
