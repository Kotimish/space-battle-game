from typing import Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    """ Структурный интерфейс (Протокол) для классов, поддерживающих сериализацию в словарь."""

    def to_dict(self) -> dict:
        """
        Сериализует объект в словарь.
        :return: Словарь с данными объекта.
        """
        raise NotImplementedError
