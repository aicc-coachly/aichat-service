from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class ChatRoom(Base):
    __tablename__ = "chat_room"

    room_id = Column(Integer, primary_key=True, index=True)
    user_number = Column(Integer, nullable=False, index=True)  # 유저 넘버 필드
    trainer_number = Column(Integer, nullable=True)  # 트레이너 넘버, 기본값은 NULL

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # user_id를 외래 키로 정의할 수도 있음
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
