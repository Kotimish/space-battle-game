import pytest

from src.factories.adaptor_factory import AdapterFactory
from src.commands.ioc_commands.init_container import InitContainerCommand
from src.commands.ioc_commands.reset_container import ResetContainerCommand
from src.dependencies.ioc import IoC
from src.interfaces.base_command import BaseCommand


@pytest.fixture(autouse=True)
def ioc_container():
    InitContainerCommand().execute()
    # Создание базового пространства
    IoC[BaseCommand].resolve('IoC.Scope.Create', 'base_game_scope').execute()
    # Установка базового пространства в качестве активного
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'base_game_scope').execute()
    # Регистрация зависимости генерации адаптеров
    adaptor_factory = lambda *args, **kwargs: AdapterFactory.get_adapter(*args, **kwargs)
    IoC[BaseCommand].resolve('IoC.Register', 'Adapter', adaptor_factory).execute()
    yield
    ResetContainerCommand().execute()
