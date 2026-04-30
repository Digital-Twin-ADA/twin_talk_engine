import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from twin_talk_engine.services.ai_client import AIClient

load_dotenv()

router = APIRouter()

ai_client = AIClient()


class ChatRequest(BaseModel):
    message: str


@router.get("/")
def read_root():
    return {"status": "AI Consultant is awake!"}


@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        reply = ai_client.chat(request.message)
        return reply

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
