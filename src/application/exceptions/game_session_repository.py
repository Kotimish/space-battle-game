from src.domain.exceptions.base_exception import BaseGameException # Предполагаем базовый класс


class GameSessionRepositoryException(BaseGameException):
    """Базовое исключение для ошибок репозитория GameSession."""


class GameSessionNotFoundException(GameSessionRepositoryException):
    """Выбрасывается, когда сессия с указанным ID не найдена."""
