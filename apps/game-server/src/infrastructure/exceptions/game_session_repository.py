from src.domain.exceptions.base_exception import BaseGameException


class GameSessionRepositoryException(BaseGameException):
    """Базовое исключение для ошибок репозитория GameSession."""


class GameSessionAlreadyExistsException(GameSessionRepositoryException):
    """Выбрасывается, когда попытка добавить сессию с уже существующим ID."""


class GameSessionRepositoryAccessException(GameSessionRepositoryException):
    """Выбрасывается при ошибках доступа к хранилищу."""