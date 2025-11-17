import jwt

from src.application.interfaces.jwt_service import IJWTService

class PyJWTService(IJWTService):
    """
    Реализация JWT-сервиса на основе библиотеки PyJWT.
    """
    def __init__(self, secret: str, algorithm: str, expire_minutes: int):
        """
        Инициализирует сервис JWT
        :param secret: Секретный ключ для подписи токенов. Должен храниться в секрете (к примеру в .env)
        :param algorithm: Алгоритм подписи (например, "HS256").
        :param expire_minutes:  Срок действия токена в минутах.
        """
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def encode(self, payload: dict) -> str:
        raise NotImplementedError("JWT encoding not implemented")
        # return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> dict:
        raise NotImplementedError("JWT decoding not implemented")
        # return jwt.decode(token, self._secret, algorithms=[self._algorithm])