import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import Groq
from pydantic import BaseModel

from twin_talk_engine import AGENT_INSTRUCTION

load_dotenv()

app = FastAPI(title="Twin Talk Engine API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"status": "AI Consultant is awake!"}


@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": AGENT_INSTRUCTION},
                {"role": "user", "content": request.message},
            ],
            model=os.getenv("MODEL_NAME", "llama-3.1-8b-instant"),
        )

        reply = chat_completion.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
