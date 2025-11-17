from fastapi.testclient import TestClient


def test_create_game_returns_full_response(test_client):
    """Тест создания игровой сессии"""
    resp = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "user_1",
            "participants": ["user_1"]
        }
    )
    data = resp.json()
    assert "created_at" in data
    assert data["participants"] == ["user_1"]


def test_create_game_empty_participants(test_client: TestClient):
    """Тест создания игровой сессии без участников"""
    resp = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "",
            "participants": []
        }
    )
    assert resp.status_code == 400


def test_create_game_duplicate_participants(test_client: TestClient):
    """Тест создания игровой сессии с дублированием участников"""
    resp = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "user_1",
            "participants": ["user_1", "user_1"]
        }
    )
    assert resp.status_code == 400
