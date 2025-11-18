from fastapi import APIRouter, HTTPException, Depends

from src.application.services.auth_service import AuthService
from src.presentation.api.dependencies import get_auth_service
from src.presentation.schemas.token_request import TokenRequest
from src.presentation.schemas.token_response import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token", response_model=TokenResponse)
async def issue_token(
        request: TokenRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Выдаёт JWT-токен участнику, если он состоит в указанной игре.
    :param request: ID игры и ID пользователя.
    :param auth_service: Сервис авторизации.
    :return: {"access_token": "...", "token_type": "bearer"}
    """
    try:
        token, expires_at = auth_service.issue_token(game_id=request.game_id, user_id=request.user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_at=expires_at
    )
