import pytest

from src.domain.models.game_session import AuthGameSession
from src.infrastructure.repositories.in_memory_auth_game_session_repository import InMemoryAuthGameSessionRepository


def test_create_duplicate_game_id():
    """Тест создания дублей"""
    repository = InMemoryAuthGameSessionRepository()
    session1 = AuthGameSession(
        "game_1",
        "user_1",
        ["user_1"]
    )
    repository.create(session1)
    session2 = AuthGameSession(
        "game_1",
        "user_2",
        ["user_2"]
    )
    with pytest.raises(ValueError):
        repository.create(session2)


def test_get_by_id_not_found():
    """Тест попытки получения несуществующего id"""
    repository = InMemoryAuthGameSessionRepository()
    assert repository.get_by_id("missing_id") is None


def test_get_all_game_ids():
    """Тест получения всех id"""
    repository = InMemoryAuthGameSessionRepository()
    repository.create(
            AuthGameSession(
            "game_1",
            "user_1",
            ["user_1"]
        )
    )
    repository.create(
        AuthGameSession(
        "game_2",
        "user_2",
        ["user_2"]
        )
    )
    ids = set(repository.get_all_game_ids())
    assert ids == {"game_1", "game_2"}
