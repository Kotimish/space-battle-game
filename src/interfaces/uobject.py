from abc import ABC, abstractmethod
from typing import Any


class UObject(ABC):
    @abstractmethod
    def get_property(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set_property(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_property(self, key: str) -> bool:
        raise NotImplementedError
