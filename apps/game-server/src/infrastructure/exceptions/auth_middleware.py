from src.domain.exceptions.base_exception import BaseGameException


class TokenException(BaseGameException):
    """Базовый класс для ошибок аутентификации"""


class MissingTokenError(TokenException):
    """Отсутствует токен аутентификации"""


class InvalidTokenError(TokenException):
    """Некорректный токен аутентификации"""


class ExpiredTokenError(TokenException):
    """Истекший токен аутентификации"""
