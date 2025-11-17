from pydantic import BaseModel


class CreateGameRequest(BaseModel):
    organizer_id: str
    participants: list[str]
