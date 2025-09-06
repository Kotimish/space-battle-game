import pytest

import src.exceptions.ioc as exceptions
from src.dependencies.ioc import IoC


def test_root_scope():
    """Тест получения корневой области (root scope)."""
    root_scope = IoC.resolve('IoC.Scope.Current').execute()
    assert root_scope == 'root'


def test_create_new_scope():
    """Тест создания новой области (scope) для изоляции зависимостей."""
    scope_name = 'test_scope'
    scope = IoC.resolve('IoC.Scope.Create', scope_name).execute()
    assert scope == scope_name


def test_create_exist_scope():
    """Тест создания уже существующей области (scope)"""
    scope_name = 'test_scope'
    IoC.resolve('IoC.Scope.Create', scope_name).execute()
    with pytest.raises(exceptions.ScopeAlreadyExistsError) as e:
        IoC.resolve('IoC.Scope.Create', scope_name).execute()


def test_set_new_scope():
    """Тест установки области (scope) активной."""
    scope_name = 'test_scope'
    scope = IoC.resolve('IoC.Scope.Create', scope_name).execute()
    IoC.resolve('IoC.Scope.Set', scope).execute()
    scope = IoC.resolve('IoC.Scope.Current').execute()

    assert scope == scope_name

def test_set_invalid_scope():
    """Тест установки активной несуществующей области (scope)"""
    with pytest.raises(exceptions.ScopeNotFoundError) as e:
        IoC.resolve('IoC.Scope.Set', 'invalid_scope_name').execute()


def test_missing_parent_scope():
    """Тест текущей области (scope) без родительской."""
    with pytest.raises(exceptions.ParentScopeNotFoundError) as e:
        IoC.resolve('IoC.Scope.Parent').execute()


def test_parent_scope():
    """Тест родительской области (scope)."""
    scope_name = 'test_scope'
    test_scope = IoC.resolve('IoC.Scope.Create', scope_name).execute()
    IoC.resolve('IoC.Scope.Set', test_scope).execute()

    current_scope = IoC.resolve('IoC.Scope.Current').execute()
    parent_scope = IoC.resolve('IoC.Scope.Parent').execute()

    assert current_scope == scope_name
    assert parent_scope == 'root'


def test_resolve_dependency_from_parent():
    """Тест регистрация и разрешения зависимости в IoC-контейнере в родительской области (scope)."""
    # Первую область (scope) с зависимостью
    scope_1 = IoC.resolve('IoC.Scope.Create', 'scope_1').execute()
    IoC.resolve('IoC.Scope.Set', scope_1).execute()
    # Регистрируем зависимость
    strategy = lambda: 'test_value'
    IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()
    # Вторую область (scope) без зависимости
    scope_2 = IoC.resolve('IoC.Scope.Create', 'scope_2').execute()
    IoC.resolve('IoC.Scope.Set', scope_2).execute()
    # Разрешаем зависимость
    result = IoC.resolve('test_strategy')
    assert result == 'test_value'


def test_pop_scope():
    """Тест удаления текущей области (scope)."""
    scope_1 = IoC.resolve('IoC.Scope.Create', 'scope_1').execute()
    IoC.resolve('IoC.Scope.Set', scope_1).execute()
    scope_2 = IoC.resolve('IoC.Scope.Create', 'scope_2').execute()
    IoC.resolve('IoC.Scope.Set', scope_2).execute()
    # Удаляем скоуп
    deleted_scope_name = IoC.resolve('IoC.Scope.Pop').execute()
    parent_scope_name = IoC.resolve('IoC.Scope.Current').execute()

    assert deleted_scope_name == scope_2
    assert parent_scope_name == scope_1


def test_reset_scope():
    """Тест полного сброса всех областей (scope)."""
    scope_1 = IoC.resolve('IoC.Scope.Create', 'scope_1').execute()
    IoC.resolve('IoC.Scope.Set', scope_1).execute()
    scope_2 = IoC.resolve('IoC.Scope.Create', 'scope_2').execute()
    IoC.resolve('IoC.Scope.Set', scope_2).execute()
    # Удаляем все скоупы
    IoC.resolve('IoC.Scope.Reset').execute()
    parent_scope_name = IoC.resolve('IoC.Scope.Current').execute()

    assert parent_scope_name == 'root'


def test_multiple_scopes():
    """Тест изоляции областей (scope) между собой."""
    # Регистрация первого scope
    scope_1 = IoC.resolve('IoC.Scope.Create', 'scope_1').execute()
    IoC.resolve('IoC.Scope.Set', scope_1).execute()
    IoC.resolve('IoC.Register', 'test_strategy_1', lambda: 'result_1').execute()
    # Сброс к корневой области (root scope)
    IoC.resolve('IoC.Scope.Set', 'root').execute()
    # Регистрация второй области (scope)
    scope_2 = IoC.resolve('IoC.Scope.Create', 'scope_2').execute()
    IoC.resolve('IoC.Scope.Set', scope_2).execute()
    IoC.resolve('IoC.Register', 'test_strategy_2', lambda: 'result_2').execute()
    # Проверка вызова зависимости из области 1 в области 2
    with pytest.raises(exceptions.DependencyNotFoundError) as e:
        IoC.resolve('test_strategy_1')
    # Проверка вызова зависимости из области 2 в области 1
    IoC.resolve('IoC.Scope.Set', 'scope_1').execute()
    with pytest.raises(exceptions.DependencyNotFoundError) as e:
        IoC.resolve('test_strategy_2')
