from src.infrastructure.factories.auth_game_session_factory import InMemoryAuthGameSessionFactory


def test_in_memory_factory_creates_valid_session():
    """Тест создания фабрикой игровой сессии"""
    factory = InMemoryAuthGameSessionFactory()
    session = factory.create(
        "user_1",
        ["user_1", "user_2"]
    )
    assert isinstance(session.game_id, str)
    assert session.game_id.startswith("battle_")
    assert session.participants == {"user_1", "user_2"}
