from src.domain.interfaces.base_query import BaseQuery
from src.domain.interfaces.uobject import UObject


class GetAllObjectsCommand(BaseQuery):
    """Команда получения информации о состоянии игровой сессии"""
    def __init__(self, game_objects: dict[str, UObject]):
        self._game_objects = game_objects

    def execute(self) -> dict[str, UObject]:
        return self._game_objects
