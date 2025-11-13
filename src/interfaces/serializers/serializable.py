from typing import Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    """Структурный интерфейс (Протокол) для классов, поддерживающих сериализацию/десериализацию в словарь."""

    def serialize(self) -> dict:
        """
        Сериализует объект в словарь.
        :return: Словарь с данными объекта.
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls,  data: dict) -> "Serializable":
        """
        Десериализует словарь в объект.
        :return: Объект класса.
        """
        raise NotImplementedError
