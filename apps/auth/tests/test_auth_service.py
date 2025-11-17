from fastapi import FastAPI, Request

from src.application.services.auth_service import AuthService
from src.presentation.api.dependencies import get_auth_service
from src.presentation.lifespan import setup_auth_service


def test_get_auth_service_via_request_state():
    """Тест настройки сервиса авторизации"""
    # Создаём приложение
    app = FastAPI()

    # Инициализируем auth_service
    auth_service: AuthService = setup_auth_service()
    app.state.auth_service = auth_service

    # Создаём фиктивный запрос с привязкой к этому приложению
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "app": app,
    }
    request = Request(scope)

    # Вызываем зависимость
    service = get_auth_service(request)

    # Проверяем, что это тот же объект
    assert service is auth_service
