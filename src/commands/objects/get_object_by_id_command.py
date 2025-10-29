from concurrent.futures import Future

from src.dependencies.ioc import IoC
from src.interfaces.base_command import BaseCommand
from src.interfaces.uobject import UObject


class GetObjectByIdCommand(BaseCommand):
    """Команда получения информации о состоянии игрового объекта в сессии"""
    def __init__(self, object_id: str, future: Future):
        self.object_id = object_id
        self.future = future

    def execute(self) -> None:
        try:
            # Получение из скоупа текущей сессии словарь игровых объектов
            game_object = IoC[UObject].resolve('Game.Object.Get', self.object_id)
            self.future.set_result(game_object.to_dict())
        except Exception as e:
            self.future.set_exception(e)
