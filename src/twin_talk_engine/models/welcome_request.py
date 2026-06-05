from pydantic import BaseModel


class WelcomeRequest(BaseModel):
    session_id: str
    user_name: str
