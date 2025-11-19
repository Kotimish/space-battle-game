from abc import ABC, abstractmethod
from typing import Any


class IDependencyResolver(ABC):
    """Интерфейс стратегии разрешения зависимости в IoC-контейнере"""
    @abstractmethod
    def resolve(self, dependency: str, *args, **kwargs) -> Any:
        raise NotImplementedError
