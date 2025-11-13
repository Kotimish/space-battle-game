from pydantic import BaseModel

class CreateGameRequest(BaseModel):
    game_type: str = "default"
