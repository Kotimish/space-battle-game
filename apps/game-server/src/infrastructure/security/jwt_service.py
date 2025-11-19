import jwt

from src.application.interfaces.jwt_service import IJWTService
from src.infrastructure.exceptions import jwt_exceptions as exceptions


class PyJWTService(IJWTService):
    """
    Реализация JWT-сервиса на основе библиотеки PyJWT.
    """

    def __init__(self, public_key: str, algorithm: str):
        """
        Инициализирует сервис JWT
        :param public_key: Публичный ключ в формате PEM (строка).
        :param algorithm: Алгоритм подписи (например, "HS256").
        """
        self._public_key = public_key
        self._algorithm = algorithm

    def encode(self, payload: dict) -> str:
        # В auth encode почти не используется, но оставим для полноты
        # Для encode нужен приватный ключ — его нет, поэтому не реализуем
        raise NotImplementedError("Encoding is not supported in Game-Server for RS256")

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._public_key, algorithms=[self._algorithm])
            return payload
        except jwt.PyJWTError as e:
            raise exceptions.JWTVerificationError(f"Invalid JWT token: {e}") from e
