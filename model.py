from sqlalchemy import Column, Integer, DECIMAL, Text, DateTime, ForeignKey, Date,Boolean 
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
    room_id = Column(Integer, index=True)  # user_id를 외래 키로 정의할 수도 있음
    sender_name = Column(Text, nullable=False)
    content= Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

class UserInbody(Base):
    __tablename__ = "user_inbody"

    user_inbody_number = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_height = Column(DECIMAL(5, 2), nullable=False)
    user_weight = Column(DECIMAL(5, 2), nullable=False)
    user_body_fat_percentage = Column(DECIMAL(5, 2), nullable=False)
    user_body_fat_mass = Column(DECIMAL(5, 2), nullable=False)
    user_muscle_mass = Column(DECIMAL(5, 2), nullable=False)
    user_metabolic_rate = Column(Integer)
    user_abdominal_fat_amount = Column(DECIMAL(3, 2))
    user_visceral_fat_level = Column(Integer)
    user_total_body_water = Column(DECIMAL(5, 2))
    user_protein = Column(DECIMAL(5, 2))
    user_measurement_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    delete_at = Column(DateTime, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    user_number = Column(Integer, ForeignKey("users.user_number"))