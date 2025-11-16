import pytest

from src.infrastructure.commands.ioc_commands.init_container import InitContainerCommand
from src.infrastructure.commands.ioc_commands.reset_container import ResetContainerCommand
from src.infrastructure.dependencies.ioc import IoC
from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler


@pytest.fixture(autouse=True)
def ioc_container():
    InitContainerCommand().execute()
    yield
    ResetContainerCommand().execute()


@pytest.fixture(autouse=True)
def register_event_loop_command(ioc_container):
    """Регистрация event-loop в IoC"""
    # Необходимо создать новую область, так как по умолчанию доступна только корневая область
    scope = IoC.resolve('IoC.Scope.Create', 'main_scope').execute()
    IoC.resolve('IoC.Scope.Set', scope).execute()
    # Регистрируем event-loop
    strategy = lambda *args, **kwargs: ThreadedCommandHandler()
    IoC.resolve('IoC.Register', 'ThreadedCommandHandler', strategy).execute()


@pytest.fixture()
def event_loop() -> ThreadedCommandHandler:
    """Получение потокового event-loop"""
    return IoC[ThreadedCommandHandler].resolve("ThreadedCommandHandler")
