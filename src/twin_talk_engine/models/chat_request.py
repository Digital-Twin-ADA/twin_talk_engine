from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    user_name: str
    message: str
