import jwt

from src.application.interfaces.jwt_service import IJWTService


class PyJWTService(IJWTService):
    """
    Реализация JWT-сервиса на основе библиотеки PyJWT.
    """

    def __init__(self, private_key: str, algorithm: str, expire_minutes: int):
        """
        Инициализирует сервис JWT
        :param private_key: Приватный ключ в формате PEM (строка).
        :param algorithm: Алгоритм подписи (например, "HS256").
        :param expire_minutes:  Срок действия токена в минутах.
        """
        self._private_key = private_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self._private_key, algorithm=self._algorithm)

    def decode(self, token: str) -> dict:
        # В auth decode почти не используется, но оставим для полноты
        # Для decode нужен публичный ключ — его нет, поэтому не реализуем
        raise NotImplementedError("Decoding is not supported in Auth service for RS256")
