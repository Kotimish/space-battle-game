from src.domain.interfaces.base_query import BaseQuery
from src.domain.interfaces.uobject import UObject


class GetObjectByIdCommand(BaseQuery):
    """Команда получения информации о состоянии игрового объекта в сессии"""

    def __init__(self, game_objects: dict[str, UObject], object_id: str):
        self._game_objects = game_objects
        self._object_id = object_id

    def execute(self) -> UObject:
        return self._game_objects.get(self._object_id)
