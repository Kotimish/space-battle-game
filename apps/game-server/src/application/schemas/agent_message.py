from pydantic import BaseModel, Field


class AgentMessage(BaseModel):
    game_id: str
    user_id: str
    object_id: str
    operation_id: str
    arguments: dict

    def __str__(self):
        return f"Game: {self.game_id}; User: {self.user_id}; Object: {self.object_id}; Operation: {self.operation_id}; Arguments: {self.arguments}"
