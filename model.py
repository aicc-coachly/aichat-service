from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from db_setup import Base

class ChatRoom(Base):
    __tablename__ = "chat_room"
    room_id = Column(Integer, primary_key=True, index=True)
    user_number = Column(Integer, nullable=False, index=True)  # 유저 넘버 필드
    trainer_number = Column(Integer, nullable=True)  # 트레이너 넘버, 기본값은 NULL

class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_number = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, index=True)  
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class TrainerImage(Base):
    __tablename__ = "trainer_image"
    trainer_img_number = Column(Integer, primary_key=True, index=True)
    trainer_number = Column(Integer, index=True, nullable=False)
    resume = Column(String, nullable=True)

class Trainer(Base):
    __tablename__ = "trainers"
    trainer_number = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)