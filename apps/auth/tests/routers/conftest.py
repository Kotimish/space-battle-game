import pytest
from fastapi.testclient import TestClient

from src.presentation.app import app


@pytest.fixture
def test_client():
    """
    Тестовый клиент для обмена сообщений с тестируемым сервером.
    По умолчанию использует lifespan веб-фреймворка FastApi.
    """
    with TestClient(app) as client:
        yield client
