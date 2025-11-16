from fastapi import APIRouter, HTTPException, Depends

from src.presentation.api.dependencies import get_game_service
from src.application.exceptions.game_session import GameNotFoundError
from src.application.services.game_service import GameService
from src.application.schemas.agent_message import AgentMessage
from src.presentation.schemas.create_game_request import CreateGameRequest

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.post('/command')
async def accept_agent_command(
    message: AgentMessage,
    game_service: GameService = Depends(get_game_service)
):
    """
    Принимает и ставит в очередь команду от игрового агента для выполнения
    :param message: Сообщение от агента, содержащее идентификатор игровой сессии (`game_id`) и данные команды
    :param game_service: Сервис игровых сессий.
    :raises HTTPException: Ошибка постановки команды в очередь.
    :return: Словарь с ключом "status": "accepted", если команда успешно поставлена в очередь.
    """
    try:
        game_service.execute_command(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Command failed: {str(e)}")
    else:
        return {"status": "accepted"}


@router.post('/')
async def create_game_session(
    request: CreateGameRequest,
    game_service: GameService = Depends(get_game_service)
):
    """
    Создание новой изолированной игровой сессии.

    Инициализирует внутреннее состояние сессии (очередь команд, реестр объектов и т.д.)
    и возвращает уникальный идентификатор, который клиенты используют для взаимодействия
    с этой сессией.
    :param request: Информация о типе игровой сессии, определяющей правила игры.
    :param game_service: Сервис игровых сессий.
    :return: Словарь с ключом "game_id" и строковым представлением UUID сессии.
    """
    game_id = game_service.create_game(ruleset=request.game_type)
    return {"game_id": str(game_id)}


@router.delete('/{game_id}')
async def delete_game_session(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Завершение и освобождение ресурсов указанной игровой сессии
    :param game_id: Идентификатор игровой сессии.
    :param game_service: Сервис игровых сессий.
    :return: Словарь с ключом `"status": "terminated"`, подтверждающий завершение.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена;
    """
    try:
        game_service.stop_game(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    return {"status": "terminated"}


@router.get('/')
async def get_game_info(
    game_service: GameService = Depends(get_game_service)
):
    """
    Возвращает информацию обо всех игровых сессиях.

    :param game_service: Сервис игровых сессий.
    :return: Словарь в формате {"games": {<game_id>: <game_info>, ...}},
             где <game_id> — уникальный идентификатор сессии,
             а <game_info> — соответствующие данные сессии.
    :raises HTTPException:
        Код 504, если обработчик не вернул результат в течение 5 секунд.
    """
    games = game_service.get_list_all_games()
    return {
        "games":{
            "id": game
            for game in games
        }
    }


@router.get('/{game_id}')
async def get_game_info(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Возвращает информацию об игровой сессии по её идентификатору.

    :param game_id: Идентификатор игровой сессии.
    :param game_service: Сервис игровых сессий.
    :return: Словарь с ключами:
             — "id": идентификатор сессии (str),
             — "status": текущий статус сессии (например, "active").
             В будущем планируется расширение ответа.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена.
    """
    try:
        status = game_service.get_game_state(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    return status
