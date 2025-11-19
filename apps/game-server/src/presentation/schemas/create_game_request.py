from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    game_id: str = Field(..., description="ID игры, сгенерированный в auth микросервисе.")
    user_id: str = Field(..., description="ID пользователя, инициирующего создание сессии.")
    game_type: str = Field(default="default", description="Тип правил игры.")
