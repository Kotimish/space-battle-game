from fastapi.testclient import TestClient


def test_create_game_returns_full_response(test_client: TestClient):
    """Тест создания игровой сессии и проверки полного ответа"""
    organizer_id = "user_1"
    participants_list = ["user_1", "user_2"]
    create_data = {
        "organizer_id": organizer_id,
        "participants": participants_list
    }

    response = test_client.post("/api/games/", json=create_data)
    assert response.status_code == 200

    data = response.json()

    # Проверяем, что в ответе есть все ожидаемые поля
    assert "game_id" in data
    game_id = data.get("id") or data.get("game_id")
    assert game_id is not None
    assert isinstance(game_id, str)
    assert "created_at" in data

    # Проверяем список участников
    assert "participants" in data
    assert sorted(data["participants"]) == sorted(participants_list)

    # Проверяем, что организатор в списке участников
    assert organizer_id in data["participants"]


def test_create_game_empty_participants(test_client: TestClient):
    """Тест создания игровой сессии без участников"""
    response = test_client.post("/api/games/", json={
        "organizer_id": "user_1",
        "participants": []
    })

    assert response.status_code == 422


def test_create_game_duplicate_participants(test_client: TestClient):
    """Тест создания игровой сессии с дублированием участников"""
    response = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "user_1",
            "participants": ["user_1", "user_1"]
        }
    )
    assert response.status_code == 400
