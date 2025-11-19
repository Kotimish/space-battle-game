from pydantic import BaseModel, Field


class DeleteGameResponse(BaseModel):
    status: str = Field(..., description="Статус удаляемой игры.")
