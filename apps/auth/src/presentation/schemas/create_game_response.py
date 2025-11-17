from datetime import datetime

from pydantic import BaseModel


class CreateGameResponse(BaseModel):
    game_id: str
    participants: list[str]
    created_at: datetime
