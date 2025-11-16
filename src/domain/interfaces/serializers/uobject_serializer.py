from abc import ABC, abstractmethod
from src.domain.interfaces.uobject import UObject

class IGameObjectSerializer(ABC):
    """Интерфейс сериализации/десериализации в словарь для класса универсального объекта."""
    @abstractmethod
    def serialize(self, obj: UObject) -> dict:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self,  data: dict) -> UObject:
        raise NotImplementedError