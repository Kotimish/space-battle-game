from fastapi.testclient import TestClient

from tests.helpers.jwt_utils import create_test_token


def test_games_create_no_token_needed(test_client: TestClient):
    """
    Тест публичного эндпоинт без необходимости проверки токена
    """
    response = test_client.get("/api/games")
    assert response.status_code == 200


def test_games_command_with_valid_token(test_client: TestClient):
    """
    Тест запроса с JWT-токеном
    """
    user_id = "user_0"
    game_id = "game_0"

    # Генерация токена
    token = create_test_token(game_id=game_id, user_id=user_id)

    # Создаём игру
    response = test_client.post(
        "/api/games",
        json={
            "user_id": user_id,
            "game_id": game_id,
            "game_type": "test",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    game_id = response.json()["game_id"]

    # Отправляем команду с токеном
    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_id,
            "user_id": user_id,
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
    user_id = "user_0"
    game_id = "game_0"
    response = test_client.post(
        "/api/games",
        json={
            "user_id": user_id,
            "game_id": game_id,
            "game_type": "test",
        }
    )
    assert response.status_code == 401


def test_games_command_invalid_token(test_client: TestClient):
    """
    Тест запроса с невалидным токеном
    """
    # Невалидный JWT
    user_id = "user_0"
    game_id = "game_0"
    fake_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx"
    response = test_client.post(
        "/api/games",
        json={
            "game_type": "test",
            "user_id": user_id,
            "game_id": game_id,
        },
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    assert response.status_code == 401


def test_games_command_game_id_mismatch(test_client: TestClient):
    """
    Тест запроса с разными id игровой сессии в сообщении и в токене
    """

    # Создаём две игры
    # Первая игра
    game_1_user_id = "user_0"
    game_1_id = "game_0"
    # Генерация токена
    token_1 = create_test_token(game_id=game_1_id, user_id=game_1_user_id)
    response = test_client.post(
        "/api/games",
        json={
            "game_type": "test",
            "user_id": game_1_user_id,
            "game_id": game_1_id,
        },
        headers={"Authorization": f"Bearer {token_1}"}
    )
    assert response.status_code == 200
    game_1 = response.json()["game_id"]

    # Вторая игра
    game_2_user_id = "user_1"
    game_2_id = "game_1"
    # Генерация токена
    token_2 = create_test_token(game_id=game_2_id, user_id=game_2_user_id)
    response = test_client.post(
        "/api/games",
        json={
            "game_type": "test",
            "user_id": game_2_user_id,
            "game_id": game_2_id,
        },
        headers={"Authorization": f"Bearer {token_2}"}
    )
    assert response.status_code == 200
    game_2 = response.json()["game_id"]

    # Запрос для game_2 с токеном от game_1 → ошибка
    response = test_client.post(
        "/api/games/command",
        json={
            "game_id": game_2,
            "object_id": "object_0",
            "operation_id": "movement",
            "arguments": {"velocity": {"x": 10, "y": 0}}
        },
        headers={"Authorization": f"Bearer {token_1}"}
    )
    assert response.status_code == 403
    assert "Token game_id does not match request game_id" in response.json()["detail"]
