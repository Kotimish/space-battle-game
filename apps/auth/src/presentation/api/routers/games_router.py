from fastapi import APIRouter, HTTPException, Depends
from src.application.services.auth_service import AuthService
from src.presentation.api.dependencies import get_auth_service
from src.presentation.schemas.create_game_request import CreateGameRequest

router = APIRouter(
    prefix="/games",
    tags=["games"]
)

@router.post("/", response_model=dict[str, str])
async def create_game(
    request: CreateGameRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Создаёт новую игровую сессию и возвращает её идентификатор.
    :param request: Список user_id участников.
    :param auth_service: Сервис авторизации.
    :return: Словарь с ключом "game_id" и значением с id игровой сессии.
    """
    if not request.participants:
        raise HTTPException(status_code=400, detail="Participants list cannot be empty")
    if len(set(request.participants)) != len(request.participants):
        raise HTTPException(status_code=400, detail="Participants must be unique")

    game_id = auth_service.create_game(participants=request.participants)
    return {"game_id": game_id}