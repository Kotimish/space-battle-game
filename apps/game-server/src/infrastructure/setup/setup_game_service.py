from src.application.services.game_service import GameService
from src.application.services.ruleset_resolver import RulesetResolver
from src.infrastructure.executors.command_executor import CommandExecutor
from src.infrastructure.factories.command_handler.threaded_command_handler_factory import ThreadedCommandHandlerFactory
from src.infrastructure.factories.game_session_factory import GameSessionFactory
from src.infrastructure.repositories.game_session_repository import InMemoryGameSessionRepository
from src.infrastructure.rules import DefaultRuleset, TestRuleset, StandardBattleRuleset


def setup_game_service() -> GameService:
    """
    Инициализирует менеджер игровых сессий и регистрирует его в IoC-контейнере.
    """
    # Создание репозитория
    session_repository = InMemoryGameSessionRepository()
    # Создание обработчика очереди команд
    command_handler_factory = ThreadedCommandHandlerFactory()
    # Создание разрешителя правил
    rulesets = {
        "default": DefaultRuleset(),
        "test": TestRuleset(),
        "standard": StandardBattleRuleset(),
    }
    ruleset_resolver = RulesetResolver(rulesets)
    command_executor = CommandExecutor(session_repository, command_handler_factory, ruleset_resolver)
    session_factory = GameSessionFactory()
    # Создание основного сервис для работы с игровой сессией
    game_service = GameService(command_executor, session_repository, session_factory)

    return game_service
