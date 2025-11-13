from threading import Lock

from src.exceptions import game_object as exceptions
from src.interfaces.uobject import UObject


class GameSession:
    """
    Агрегат, представляющий одну игровую сессию.
    """

    def __init__(self, game_id: str):
        self.id = game_id
        # Словарь игровых объектов, принадлежащих этой сессии
        self._objects: dict[str, UObject] = {}
        # Активность
        self._is_active = False
        # Для потокобезопасности
        self._lock = Lock()

    def add_object(self, obj_id: str, obj: UObject) -> None:
        """Добавление нового объекта в сессию"""
        with self._lock:
            if obj_id in self._objects:
                raise exceptions.ObjectAlreadyExistsError(f"Object {obj_id} already exists")
            self._objects[obj_id] = obj

    def get_object_by_id(self, obj_id: str) -> UObject:
        """Получить объект из сессии"""
        with self._lock:
            if obj_id not in self._objects:
                raise exceptions.ObjectNotFoundError(f"Object '{obj_id}' does not found.")
            return self._objects[obj_id]

    def get_all_objects(self) -> dict[str, UObject]:
        """Получить все объекты из сессии"""
        with self._lock:
            return self._objects.copy()

    def delete_object(self, obj_id: str) -> None:
        """Удалить объект из сессии"""
        with self._lock:
            if obj_id not in self._objects:
                raise exceptions.ObjectNotFoundError(f"Object '{obj_id}' does not found.")
            self._objects.pop(obj_id)
