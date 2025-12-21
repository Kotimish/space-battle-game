from src.application.interfaces.command_executor import ICommandExecutor
from src.application.interfaces.command_handler import ICommandHandler
from src.application.interfaces.factories.command_handler_factory import ICommandHandlerFactory
from src.application.schemas.agent_message import AgentMessage
from src.application.services.ruleset_resolver import RulesetResolver
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.repositories.game_session_repository import IGameSessionRepository
from src.infrastructure.commands.control.soft_stop_command import SoftStopCommand
from src.infrastructure.commands.interpret_command import InterpretCommand
from src.infrastructure.dependencies.ioc import IoC


class CommandExecutor(ICommandExecutor):
    def __init__(
            self,
            repository: IGameSessionRepository,
            handler_factory: ICommandHandlerFactory,
            ruleset_resolver: RulesetResolver
    ):
        self._repository = repository
        self._factory = handler_factory
        self._handlers: dict[str, ICommandHandler] = {}
        self._ruleset_resolver = ruleset_resolver

    def start(self, game_id: str, ruleset: str = "default") -> None:
        session = self._repository.get_by_id(game_id)
        ruleset = self._ruleset_resolver.get_ruleset(ruleset)
        # Добавляем объекты
        initial_objects = ruleset.get_initial_objects()
        for obj_id, obj in initial_objects.items():
            session.add_object(obj_id, obj)
        # Регистрируем зависимости
        dependencies = ruleset.get_dependencies(game_id, session)
        init_commands = [
            IoC[BaseCommand].resolve('IoC.Register', dependency_name, dependency)
            for dependency_name, dependency in dependencies.items()
        ]
        # Создаем обработчик очереди команд
        handler = self._factory.create(game_id, init_commands)
        self._handlers[game_id] = handler
        handler.start()

    def stop(self, game_id: str) -> None:
        if game_id in self._handlers:
            handler = self._handlers.pop(game_id)
            handler.enqueue_command(SoftStopCommand())

    def stop_all(self) -> None:
        for handler in self._handlers.values():
            handler.enqueue_command(SoftStopCommand())


    def enqueue_interpret_command(self, game_id: str, message: AgentMessage) -> None:
        handler = self._handlers[game_id]
        cmd = InterpretCommand(message=message)
        handler.enqueue_command(cmd)