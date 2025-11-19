from fastapi.testclient import TestClient


def test_app_startup(test_client: TestClient):
    """Тест запуска приложения"""
    response = test_client.get("/api/health/")
    assert response.status_code == 200
