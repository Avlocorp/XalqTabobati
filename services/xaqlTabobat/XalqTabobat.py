from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, select, create_engine

from Settings import ServerDbUrl
from models.models import Chats, ChatMessages
from services.xaqlTabobat.MLModel import model_tibb

modelTib = APIRouter()
engine = create_engine(ServerDbUrl)
class MessagePart(BaseModel):
    role: str
    parts: str

class MessagesRequest(BaseModel):
    message: str
    unique_id: str

class SingleMessageRequest(BaseModel):
    unique_id: str

@modelTib.post("/message-bot/")
async def messageBot(request: MessagesRequest):

    try:
        messsageHistory = get_or_create_chat(
            unique_id=request.unique_id,
            message=request.message,
            role='user'
        )
        chat_session = model_tibb.start_chat(history=messsageHistory['formatted_messages'])
        response = chat_session.send_message(request.message)
        return {
            "result": response.text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the message: {str(e)}")


@modelTib.get("/get-messages")
async def getMessages(request: SingleMessageRequest):
    try:
        with Session(engine) as session:
            chat = session.exec(select(Chats).where(Chats.unique_id == request.unique_id)).first()
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            messages = session.exec(select(ChatMessages).where(ChatMessages.chat_id == chat.id)).all()

            return {"messages": messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving messages: {str(e)}")




def get_or_create_chat(unique_id: str, message: str, role:str) :
    with Session(engine) as session:
        chat = session.exec(select(Chats).where(Chats.unique_id == unique_id)).first()

        if chat is None:
            chat = Chats(unique_id=unique_id)
            session.add(chat)
            session.commit()
            session.refresh(chat)

        new_message = ChatMessages(chat_id=chat.id, message=message, role=role)
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        messages = session.exec(select(ChatMessages).where(ChatMessages.chat_id == chat.id)).all()
        formatted_messages = [{"role": msg.role, "parts": [msg.message]} for msg in messages]

        return {"formatted_messages":formatted_messages, "unformatted_messages":messages}
