import logging

from src.application.exceptions import game_session_repository as exceptions
from src.application.interfaces.command_executor import ICommandExecutor
from src.application.interfaces.factories.game_session_factory import IGameSessionFactory
from src.application.schemas.agent_message import AgentMessage
from src.domain.interfaces.repositories.game_session_repository import IGameSessionRepository
from src.domain.interfaces.uobject import UObject
from src.domain.models.game_session import GameSession

logger = logging.getLogger(__name__)


class GameService:
    def __init__(
            self,
            command_executor: ICommandExecutor,
            repository: IGameSessionRepository,
            session_factory: IGameSessionFactory,
    ):
        self._repository = repository
        self._command_executor = command_executor
        self._session_factory = session_factory

    def create_game(self, ruleset: str = "default", participants: list[str] = None) -> str:
        """Создаёт новую игровую сессию, возвращает game_id"""  # Преобразуем список в множество для уникальности и передаем в фабрику
        participants_set = set(participants) if participants else set()
        session = self._session_factory.create(participants_set)
        self._repository.add(session)
        self._command_executor.start(session.id, ruleset)
        logger.info(f"Created game session {session.id} for participants {participants_set}")
        return session.id

    def create_game_with_id(self, game_id: str, ruleset: str = "default") -> str:
        """
        Создаёт новую игровую сессию с указанным game_id.
        :param game_id: Уникальный ID сессии, предоставленный извне.
        :param ruleset: Тип правил для инициализации сессии.
        :return: Id новой сессии.
        :raises GameAlreadyExistsError: Если сессия с таким game_id уже существует.
        """
        # Создаём сессию с предоставленным ID
        session = self._session_factory.create_with_id(game_id) # Вызываем фабрику, передавая ID
        self._repository.add(session)
        self._command_executor.start(session.id, ruleset)
        logger.info(f"Created game session {session.id}")
        return session.id

    def stop_game(self, game_id: str) -> None:
        """Завершает сессию и освобождает ресурсы"""
        if not self._repository.get_by_id(game_id):
            raise exceptions.GameSessionNotFoundException(f"Game '{game_id}' not found.")
        self._command_executor.stop(game_id)
        self._repository.remove(game_id)

    def stop_all_game(self) -> None:
        """Остановка всех игровых сессий"""
        self._command_executor.stop_all()
        self._repository.remove_all()

    def execute_command(self, message: AgentMessage) -> None:
        """Ставит интерпретатор сообщения в очередь указанной сессии"""
        self._command_executor.enqueue_interpret_command(message.game_id, message)

    def get_list_all_games(self) -> list[str]:
        """Возвращает названия доступным сессий"""
        sessions = self._repository.get_all()
        return [
            session.id
            for session in sessions
        ]

    def get_game_state(self, game_id: str) -> dict:
        """Возвращает состояние указанной сессии"""
        session = self._ensure_session_exists(game_id)
        return {
            "id": session.id,
            "status": "active"
            # TODO дополнить другими данными (status, number_of_players,...)
        }

    def get_all_object_state(self, game_id: str) -> dict[str, UObject]:
        """Возвращает состояние всех объектов из определенной сессии"""
        session = self._ensure_session_exists(game_id)
        return session.get_all_objects()

    def get_object_state(self, game_id: str, object_id: str) -> UObject:
        """Возвращает состояние конкретного объекта из определенной сессии"""
        session = self._ensure_session_exists(game_id)
        return session.get_object_by_id(object_id)

    def _ensure_session_exists(self, game_id: str) -> GameSession:
        session = self._repository.get_by_id(game_id)
        if not session:
            raise exceptions.GameSessionNotFoundException(f"Game '{game_id}' not found.")
        return session
