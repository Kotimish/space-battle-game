from fastapi import APIRouter, Depends

from src.api.dependencies import get_game_service, get_serializer
from src.interfaces.serializers.uobject_serializer import IGameObjectSerializer
from src.services.game_service import GameService

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get('/{game_id}/objects')
async def get_all_objects(
    game_id: str,
    game_service: GameService = Depends(get_game_service),
    serializer: IGameObjectSerializer = Depends(get_serializer),
):
    """
    Возвращает полное состояние всех объектов в указанной игровой сессии
    :param game_id: Идентификатор игровой сессии.
    :param game_service: Сервис игровых сессий.
    :param serializer: Сериалайзер/Десериалайзер.
    :return: Словарь с "game_id" и списком игровых объектов ("objects")
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена;
        код 504, если обработчик не вернул результат в течение 5 секунд.
    """
    game_objects = game_service.get_all_object_state(game_id)
    return {
        "objects": {
            key: serializer.serialize(game_object)
            for key, game_object in game_objects.items()
        }
    }


@router.get('/{game_id}/objects/{object_id}')
async def get_object_state(
    game_id: str,
    object_id: str,
    game_service: GameService = Depends(get_game_service),
    serializer: IGameObjectSerializer = Depends(get_serializer),
):
    """
    Возвращает состояние определенного игрового объекта по его идентификатору.
    :param game_id: Идентификатор игровой сессии.
    :param object_id: Идентификатор запрашиваемого объекта.
    :param game_service: Сервис игровых сессий.
    :param serializer: Сериалайзер/Десериалайзер.
    :return: Словарь с ключом "object" и информацией в виде словаря об игровом объекте.
    :raises HTTPException:
        Код 404, если сессия с указанным "game_id" не найдена.
    """
    game_object = game_service.get_object_state(game_id, object_id)
    return serializer.serialize(game_object)
