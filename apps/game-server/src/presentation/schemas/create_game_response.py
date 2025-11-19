from pydantic import BaseModel, Field


class CreateGameResponse(BaseModel):
    game_id: str = Field(..., description="ID игры, созданной в game-server микросервисе.")
