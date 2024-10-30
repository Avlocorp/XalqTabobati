from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class FirstTable(Base):
    __tablename__ = 'first_table'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    session_id = Column(String, index=True)

    messages = relationship("SecondTable", back_populates="chat")


class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey('first_table.chat_id'))
    message = Column(String)
    role = Column(String)

    # Relationship to the first table
    chat = relationship("FirstTable", back_populates="messages")
