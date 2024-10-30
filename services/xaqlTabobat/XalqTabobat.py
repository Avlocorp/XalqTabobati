from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.xaqlTabobat.MLModel import model_tibb

modelTib = APIRouter()
class MessagePart(BaseModel):
    role: str
    parts: str


class MessagesRequest(BaseModel):
    user_input: str


@modelTib.post("/message-bot/")
async def messageBot(request: MessagesRequest):

    try:
        # messages = [{"role": chat.role, "parts": [chat.parts]} for chat in request.messages]
        chat_session = model_tibb.start_chat()
        response = chat_session.send_message(request.user_input)
        return {
            "result": response.text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the message: {str(e)}")
