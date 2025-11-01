from concurrent.futures import Future

from fastapi import APIRouter, HTTPException, Depends

from src.api.dependencies import get_game_manager, wait_for_threaded_future
from src.commands.objects import GetAllObjectsCommand, GetObjectByIdCommand
from src.exceptions.game_manager import GameNotFoundError
from src.services.game_manager import GameManager

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get('/{game_id}/objects')
async def get_all_objects(
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
    return {
        "objects": result
    }


@router.get('/{game_id}/objects/{object_id}')
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
    return result
