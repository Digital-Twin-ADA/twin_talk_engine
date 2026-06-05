import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from twin_talk_engine.models.chat_request import ChatRequest
from twin_talk_engine.models.welcome_request import WelcomeRequest
from twin_talk_engine.services.ai_client import AIClient

load_dotenv()
router = APIRouter()
ai_client = AIClient()


@router.get("/")
def read_root():
    return {"status": "AI Consultant is awake!"}


@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        reply = ai_client.chat(
            session_id=request.session_id,
            user_name=request.user_name,
            user_message=request.message,
        )
        return reply

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/welcome")
def welcome_user(request: WelcomeRequest):
    try:
        reply = ai_client.get_welcome_message(
            session_id=request.session_id, user_name=request.user_name
        )
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
