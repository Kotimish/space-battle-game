from src.domain.exceptions.base_exception import BaseGameException


class RulesetException(BaseGameException):
    """Базовое исключение для шаблона игровых правил."""


class RulesetNotFoundError(RulesetException):
    """Ошибка возникает, когда шаблон игровой сессии с указанным идентификатором не существует или не найден."""
