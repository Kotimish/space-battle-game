from pydantic import BaseModel


class CreateGameRequest(BaseModel):
    participants: list[str]
