from abc import ABC, abstractmethod
from typing import Any


class UObject(ABC):
    """Интерфейс универсального объекта"""
    @abstractmethod
    def get_property(self, key: str) -> Any:
        """Возвращает значение свойства по его имени."""
        raise NotImplementedError

    @abstractmethod
    def set_property(self, key: str, value: Any) -> None:
        """Устанавливает значение свойства по его имени."""
        raise NotImplementedError

    @abstractmethod
    def check_property(self, key: str) -> bool:
        """Проверяет, существует ли свойство с указанным именем."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """"Сериализует объект в словарь для внешнего представления."""
        raise NotImplementedError
