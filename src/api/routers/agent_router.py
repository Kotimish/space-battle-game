from concurrent.futures import Future

from fastapi import APIRouter, HTTPException, Depends

from src.api.dependencies import get_game_manager, wait_for_threaded_future
from src.commands.interpret_command import InterpretCommand
from src.commands.objects import GetAllObjectsCommand, GetObjectByIdCommand
from src.exceptions.game_manager import GameNotFoundError
from src.game_manager import GameManager
from src.models.agent_message import AgentMessage

router = APIRouter(
    prefix="/game",
    tags=["game"],
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


@router.get('/{game_id}')
async def get_game_state(
    game_id: str,
    game_manager: GameManager = Depends(get_game_manager),
):
    """
    Возвращает полное состояние всех объектов в указанной игровой сессии
    :param game_id: Идентификатор игровой сессии.
    :param game_manager: Менеджер игровых сессий.
    :return: Словарь с "game_id" и списком игровых объектов ("objects")
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена;
        код 504, если обработчик не вернул результат в течение 5 секунд.
    """
    future = Future()
    try:
        command_handler = game_manager.get(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    command_handler.enqueue_command(GetAllObjectsCommand(future))

    result = await wait_for_threaded_future(future, 5.0)
    return {"game_id": game_id, "objects": result}


@router.get('/{game_id}/object/{object_id}')
async def get_object_state(
    game_id: str,
    object_id: str,
    game_manager: GameManager = Depends(get_game_manager),
):
    """
    Возвращает состояние определенного игрового объекта по его идентификатору.
    :param game_id: Идентификатор игровой сессии.
    :param object_id: Идентификатор запрашиваемого объекта.
    :param game_manager: Менеджер игровых сессий.
    :return: Словарь с ключом "object" и информацией в виде словаря об игровом объекте.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена;
        код 504, если обработчик не вернул результат в течение 5 секунд.
    """
    future = Future()

    try:
        command_handler = game_manager.get(game_id)
    except GameNotFoundError as e:
        raise HTTPException(404, f"Game '{game_id}' not found.")
    command_handler.enqueue_command(GetObjectByIdCommand(object_id, future))

    result = await wait_for_threaded_future(future, 5.0)
    return {"object": result}
