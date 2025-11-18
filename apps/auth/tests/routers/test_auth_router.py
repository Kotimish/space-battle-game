from fastapi.testclient import TestClient


def test_issue_token_game_not_found(test_client: TestClient):
    """Тест получения токена для несуществующей игры"""
    response = test_client.post(
        "/api/auth/token",
        json={
            "game_id": "battle_1",
            "user_id": "user_1"
        }
    )
    assert response.status_code == 404


def test_issue_token_user_not_in_game(test_client: TestClient):
    """Тест создания игровой сессии и получения токена к ней"""
    create_response = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "user_1",
            "participants": ["user_1"]
        }
    )
    assert create_response.status_code == 200
    game_data = create_response.json()
    game_id = game_data["game_id"]
    assert game_id

    token_resp = test_client.post(
        "/api/auth/token",
        json={
            "game_id": game_id,
            "user_id": "user_2"
        }
    )
    assert token_resp.status_code == 403


def test_issue_token_success(test_client: TestClient):
    """Тест успешного получения токена"""
    # Создаём игру с участниками
    create_response = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "user_1",
            "participants": ["user_1", "user_2"]
        }
    )
    assert create_response.status_code == 200
    game_data = create_response.json()
    game_id = game_data["game_id"]
    assert game_id

    # Вызываем эндпоинт получения токена
    token_request_data = {
        "game_id": game_id,
        "user_id": "user_2"  # user_2 является участником
    }
    response = test_client.post("/api/auth/token", json=token_request_data)
    assert response.status_code == 200

    # Проверяем структуру и содержимое ответа
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_at" in data
