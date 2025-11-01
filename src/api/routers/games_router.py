from fastapi import APIRouter, HTTPException, Depends

from src.api.dependencies import get_game_manager
from src.commands.interpret_command import InterpretCommand
from src.exceptions.game_manager import GameNotFoundError
from src.services.game_manager import GameManager
from src.models.agent_message import AgentMessage

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.post('/command')
async def accept_agent_command(
    message: AgentMessage,
    game_manager: GameManager = Depends(get_game_manager)
):
    """
    Принимает и ставит в очередь команду от игрового агента для выполнения
    :param message: Сообщение от агента, содержащее идентификатор игровой сессии (`game_id`) и данные команды
    :param game_manager: Менеджер игровых сессий.
    :raises HTTPException: Ошибка постановки команды в очередь.
    :return: Словарь с ключом "status": "accepted", если команда успешно поставлена в очередь.
    """
    try:
        command_handler = game_manager.get(message.game_id)
        cmd = InterpretCommand(message=message)
        command_handler.enqueue_command(cmd)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Command failed: {str(e)}")
    else:
        return {"status": "accepted"}


@router.post('/')
async def create_game_session(
    game_manager: GameManager = Depends(get_game_manager)
):
    """
    Создание новой изолированной игровой сессии.

    Инициализирует внутреннее состояние сессии (очередь команд, реестр объектов и т.д.)
    и возвращает уникальный идентификатор, который клиенты используют для взаимодействия
    с этой сессией.
    :param game_manager: Менеджер игровых сессий.
    :return: Словарь с ключом "game_id" и строковым представлением UUID сессии.
    """
    """Создание новой игровой сессии"""
    game_id = game_manager.create()
    return {"game_id": str(game_id)}


@router.delete('/{game_id}')
async def delete_game_session(
    game_id: str,
    game_manager: GameManager = Depends(get_game_manager)
):
    """
    Завершение и освобождение ресурсов указанной игровой сессии
    :param game_id: Идентификатор игровой сессии.
    :param game_manager: Менеджер игровых сессий.
    :return: Словарь с ключом `"status": "terminated"`, подтверждающий завершение.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена;
    """
    try:
        game_manager.stop_game(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    return {"status": "terminated"}


@router.get('/')
async def get_game_info(
    game_manager: GameManager = Depends(get_game_manager),
):
    """
    Возвращает информацию обо всех игровых сессиях.

    :param game_manager: Менеджер игровых сессий.
    :return: Словарь в формате {"games": {<game_id>: <game_info>, ...}},
             где <game_id> — уникальный идентификатор сессии,
             а <game_info> — соответствующие данные сессии.
    :raises HTTPException:
        Код 504, если обработчик не вернул результат в течение 5 секунд.
    """
    games = game_manager.get_all()
    return {
        "games":{
            "id": game
            for game in games
        }
    }


@router.get('/{game_id}')
async def get_game_info(
    game_id: str,
    game_manager: GameManager = Depends(get_game_manager),
):
    """
    Возвращает информацию об игровой сессии по её идентификатору.

    :param game_id: Идентификатор игровой сессии.
    :param game_manager: Менеджер игровых сессий.
    :return: Словарь с ключами:
             — "id": идентификатор сессии (str),
             — "status": текущий статус сессии (например, "active").
             В будущем планируется расширение ответа.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена.
    """
    try:
        command_handler = game_manager.get(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    return {
        "id": game_id,
        "status": "active"
        # TODO дополнить другими данными (status, number_of_players,...)
    }
