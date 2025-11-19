from src.domain.exceptions.base_exception import BaseGameException


class JWTException(BaseGameException):
    """Базовое исключение для JWS."""


class JWTVerificationError(JWTException):
    """Ошибка верификации JWT-токена."""
