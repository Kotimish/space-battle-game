from src.infrastructure.dependencies.ioc import IoC
from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler
from src.domain.interfaces.base_command import BaseCommand
from src.application.interfaces.command_handler import ICommandHandler
from src.application.interfaces.factories.command_handler_factory import ICommandHandlerFactory


class ThreadedCommandHandlerFactory(ICommandHandlerFactory):
    def create(self, scope_name: str, init_commands: list[BaseCommand] | None = None) -> ICommandHandler:
        # Создаём скоуп
        scope_name = IoC[BaseCommand].resolve('IoC.Scope.Create', scope_name).execute()
        # Создаём обработчик
        handler = ThreadedCommandHandler()
        # Устанавливаем скоуп в потоке
        set_scope_command = IoC[BaseCommand].resolve('IoC.Scope.Set', scope_name)
        handler.add_before_hook(set_scope_command)
        # Начальные зависимости
        if init_commands is None:
            init_commands = []
        for cmd in init_commands:
            handler.add_before_hook(cmd)
        return handler
