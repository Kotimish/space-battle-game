from fastapi import HTTPException, status, Request

from src.application.services.auth_service import AuthService


def get_auth_service(request: Request) -> AuthService:
    """
    Получение сервиса авторизации (AuthService) из состояния приложения (app.state).
    :param request: Сервис игровых сессий.
    :raises HTTPException: Выбрасывает ошибку, если сервис не был инициализирован.
    :return: Словарь с ключом "status": "accepted", если команда успешно поставлена в очередь.
    """
    auth_service = getattr(request.app.state, "auth_service", None)
    if auth_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AuthService is not initialized. Check lifespan setup."
        )
    return auth_service
