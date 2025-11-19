from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    organizer_id: str
    participants: list[str] = Field(min_length=1)
