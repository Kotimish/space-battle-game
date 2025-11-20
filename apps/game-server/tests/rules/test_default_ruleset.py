from src.infrastructure.rules.default_ruleset import DefaultRuleset


def test_get_initial_objects_returns_empty_dict():
    """
    Тест проверяет, что DefaultRuleset возвращает пустой словарь
    для начальных объектов.
    """
    ruleset = DefaultRuleset()
    initial_objects = ruleset.get_initial_objects()

    assert initial_objects == {}
    # Проверяем, что это именно dict
    assert isinstance(initial_objects, dict)


def test_get_allowed_operations_returns_empty_dict():
    """
    Тест проверяет, что DefaultRuleset возвращает пустой словарь
    для разрешённых операций.
    """
    ruleset = DefaultRuleset()
    allowed_operations = ruleset.get_allowed_operations()

    assert allowed_operations == {}
    assert isinstance(allowed_operations, dict)


def test_interface_implementation():
    """
    Тест проверяет, что DefaultRuleset реализует интерфейс IRuleset.
    """
    from src.domain.interfaces.ruleset import IRuleset
    ruleset = DefaultRuleset()
    # DefaultRuleset должен реализовывать интерфейс IRuleset
    assert isinstance(ruleset, IRuleset)
