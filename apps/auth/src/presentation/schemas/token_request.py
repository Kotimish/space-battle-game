from pydantic import BaseModel


class TokenRequest(BaseModel):
    game_id: str
    user_id: str
