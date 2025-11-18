import pytest
from fastapi.testclient import TestClient

from src.presentation.app import app
from tests.helpers.jwt_utils import create_test_token


@pytest.fixture
def valid_token_for_game(game_id: str) -> str:
    return create_test_token(game_id=game_id, user_id="user_0")


@pytest.fixture
def test_client():
    """
    Тестовый клиент для обмена сообщений с тестируемым сервером.
    По умолчанию использует lifespan веб-фреймворка FastApi.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def initial_game_objects() -> dict[str, dict]:
    """
    Предоставляет начальное состояние игровых объектов для тестов.
    """
    return {
        'object_0': {
            'position': {
                '__type__': 'Vector',
                '__data__': {'x': 0, 'y': 0}
            },
            'velocity': {
                '__type__': 'Vector',
                '__data__': {'x': 10, 'y': 0}
            },
            'fuel_level': 100,
            'fuel_consumption': 10
        }
    }


@pytest.fixture
def expected_game_objects() -> dict[str, dict]:
    """
    Предоставляет ожидаемое состояние игровых объектов после выполнения команды.
    """
    return {
        'object_0': {
            'position': {
                '__type__': 'Vector',
                '__data__': {
                    'x': 10,
                    'y': 0
                }
            },
            'velocity': {
                '__type__': 'Vector',
                '__data__': {
                    'x': 10,
                    'y': 0
                }
            },
            'fuel_level': 0,
            'fuel_consumption': 10
        }
    }
