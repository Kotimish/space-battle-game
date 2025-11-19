from abc import ABC, abstractmethod


class BaseQuery[T](ABC):
    """
    Интерфейс для запросов, возвращающих данные.
    """
    @abstractmethod
    def execute(self) -> T:
        raise NotImplementedError

    def __str__(self):
        return f'{self.__class__.__name__}'
