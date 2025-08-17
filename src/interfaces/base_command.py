from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

    def __str__(self):
        return f'{self.__class__.__name__}'
