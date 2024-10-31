from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field

Base = declarative_base()

class Chats(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    unique_id: int = Field(default=None)

class ChatMessages(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(default=None, foreign_key="chats.id")  # Reference the correct table name
    message: str = Field(sa_column=Text, default=None)
    role: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Use default_factory for dynamic values
