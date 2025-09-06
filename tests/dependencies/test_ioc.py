import pytest

import src.exceptions.ioc as exceptions
from src.dependencies.ioc import IoC


def test_resolve_dependency():
    """Тест регистрация и разрешения зависимости в IoC-контейнере."""
    # Создаем базовую область (scope)
    scope_name = IoC.resolve('IoC.Scope.Create', 'base_scope').execute()
    IoC.resolve('IoC.Scope.Set', 'base_scope').execute()
    # Регистрируем зависимость
    strategy = lambda: 'test_value'
    IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()

    # Разрешаем зависимость
    result = IoC.resolve('test_strategy')
    assert result == 'test_value'


@pytest.mark.parametrize(
    'test_args',
    [
        (['test_1']),
        (['test_1', 'test_2']),
        (['test_1', 'test_2', 'test_3']),
    ]
)
def test_resolve_dependency_with_args(test_args):
    """Тест разрешения зависимости с позиционными аргументами в IoC-контейнере."""
    # Создаем базовую область (scope)
    scope_name = IoC.resolve('IoC.Scope.Create', 'base_scope').execute()
    IoC.resolve('IoC.Scope.Set', 'base_scope').execute()
    # Регистрируем зависимость
    strategy = lambda *args: ''.join(args)
    IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()

    # Разрешаем зависимость
    result = IoC.resolve('test_strategy', *test_args)
    assert result == strategy(*test_args)


@pytest.mark.parametrize(
    'test_kwargs',
    [
        ({'args_1': 'test_1'}),
        ({'args_1': 'test_1', 'args_2': 'test_2'}),
        ({'args_1': 'test_1', 'args_2': 'test_2', 'args_3': 'test_3'}),
    ]
)
def test_resolve_dependency_with_kwargs(test_kwargs):
    """Тест разрешения зависимости с именованными аргументами в IoC-контейнере."""
    # Создаем базовую область (scope)
    scope_name = IoC.resolve('IoC.Scope.Create', 'base_scope').execute()
    IoC.resolve('IoC.Scope.Set', 'base_scope').execute()
    # Регистрируем зависимость
    strategy = lambda **kwargs: ''.join(kwargs.values())
    IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()

    # Разрешаем зависимость
    result = IoC.resolve('test_strategy', **test_kwargs)
    assert result == strategy(**test_kwargs)


def test_resolve_non_exist_dependency():
    """Тест ошибки разрешения незарегистрированной зависимости в IoC-контейнере."""
    with pytest.raises(exceptions.DependencyNotFoundError) as e:
        IoC.resolve('non-exist dependency')


def test_register_dependency_in_root_scope():
    """Попытка зарегистрировать новую область (scope) в корневой области (root scope)"""
    strategy = lambda: 'test_value'
    with pytest.raises(exceptions.ForbiddenRegistrationDependencyError) as e:
        IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()


def test_register_exist_resolve():
    """Тест регистрации уже существующей зависимости"""
    # Создаем базовую область (scope)
    scope_name = IoC.resolve('IoC.Scope.Create', 'base_scope').execute()
    IoC.resolve('IoC.Scope.Set', scope_name).execute()
    # Регистрируем зависимость
    strategy = lambda: 'test_value'
    IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()
    # Попытка зарегистрировать повторно зависимость
    with pytest.raises(exceptions.DependencyAlreadyRegisteredError) as e:
        IoC.resolve('IoC.Register', 'test_strategy', strategy).execute()
