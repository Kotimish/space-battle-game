from fastapi.testclient import TestClient

from tests.helpers.jwt_utils import create_test_token


def test_games_create_no_token_needed(test_client: TestClient):
    """
    Тест публичного эндпоинт без необходимости проверки токена
    """
    response = test_client.post("/api/games", json={"game_type": "test"})
    assert response.status_code == 200


def test_games_command_with_valid_token(test_client: TestClient):
    """
    Тест запроса с JWT-токеном
    """
    # Создаём игру
    resp = test_client.post("/api/games", json={"game_type": "test"})
    assert resp.status_code == 200
    game_id = resp.json()["game_id"]

    # Генерируем токен
    token = create_test_token(game_id=game_id, user_id="user_0")

    # Отправляем команду с токеном
    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_id,
            "object_id": "object_0",
            "operation_id": "movement",
            "arguments": {"velocity": {"x": 10, "y": 0}}
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}


def test_games_command_no_auth_header(test_client: TestClient):
    """
    Тест запроса без JWT-токена
    """
    response = test_client.post("/api/games", json={"game_type": "test"})
    game_id = response.json()["game_id"]

    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_id,
            "object_id": "object_0",
            "operation_id": "movement",
            "arguments": {"velocity": {"x": 10, "y": 0}}
        }
    )
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]


def test_games_command_invalid_token(test_client: TestClient):
    """
    Тест запроса с невалидным токеном
    """
    response = test_client.post("/api/games", json={"game_type": "test"})
    game_id = response.json()["game_id"]

    fake_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx"  # Невалидный JWT

    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_id,
            "object_id": "object_0",
            "operation_id": "movement",
            "arguments": {"velocity": {"x": 10, "y": 0}}
        },
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    assert response.status_code == 401


def test_games_command_game_id_mismatch(test_client: TestClient):
    """
    Тест запроса с разными id игровой сессии в сообщении и в токене
    """
    # Создаём две игры
    game_1 = test_client.post("/api/games", json={"game_type": "test"}).json()["game_id"]
    game_2 = test_client.post("/api/games", json={"game_type": "test"}).json()["game_id"]

    # Токен для game_1
    token = create_test_token(game_id=game_1, user_id="user_0")

    # Запрос для game_2 с токеном от game_1 → ошибка
    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_2,
            "object_id": "object_0",
            "operation_id": "movement",
            "arguments": {"velocity": {"x": 10, "y": 0}}
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert "Token game_id does not match request game_id" in response.json()["detail"]
