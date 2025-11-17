from fastapi.testclient import TestClient


def test_issue_token_game_not_found(test_client: TestClient):
    """Тест получения токена для несуществующей игры"""
    response = test_client.post("/api/auth/token", json={"game_id": "battle_1", "user_id": "user_1"})
    assert response.status_code == 404


def test_issue_token_user_not_in_game(test_client: TestClient):
    """Тест создания игровой сессии и получения токена к ней"""
    create_response = test_client.post(
        "/api/games/",
        json={
            "organizer_id": "other",
            "participants": ["other"]
        }
    )
    game_id = create_response.json()["game_id"]
    token_resp = test_client.post(
        "/api/auth/token",
        json={"game_id": game_id, "user_id": "user_1"}
    )
    assert token_resp.status_code == 403
