from pydantic import BaseModel, Field


class CommandResponse(BaseModel):
    status: str = Field(..., description="Статус успешного добавления команды в очередь игровой сессии.")
