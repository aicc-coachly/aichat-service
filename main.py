from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from chat import create_rag_chain  # AI 응답 생성 함수
from database import get_db  # 데이터베이스 연결 가져오기
from pydantic import BaseModel

from model import ChatMessage
from model import ChatRoom

app = FastAPI()

class ChatRoomRequest(BaseModel):
    user_number: int

@app.post("/chat-room/")
async def create_or_get_chat_room(request: ChatRoomRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 기존에 유저 넘버가 같고 트레이너가 NULL인 채팅방이 있는지 확인
        query = select(ChatRoom).where(ChatRoom.user_number == request.user_number, ChatRoom.trainer_number == None)
        result = await db.execute(query)
        existing_chat_room = result.scalars().first()

        if existing_chat_room:
            # 이미 존재하는 채팅방이 있다면, 해당 채팅방의 ID를 반환
            return {"message": "Chat room already exists", "chat_room_id": existing_chat_room.room_id}

        # 존재하지 않으면 새로운 채팅방 생성
        new_chat_room = ChatRoom(user_number=request.user_number, trainer_number=None)
        db.add(new_chat_room)
        await db.commit()
        await db.refresh(new_chat_room)
        
        return {"message": "New chat room created", "chat_room_id": new_chat_room.room_id}

    except SQLAlchemyError as e:
        await db.rollback()
        print(e)  # 오류 메시지 로그
        raise HTTPException(status_code=500, detail="Failed to create or retrieve chat room")

# 사용자 메시지 캐시용 딕셔너리
message_cache = {}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    room_id = None
    try:
        while True:
            # 클라이언트에서 JSON 형식으로 room_id와 question을 받아 처리
            data = await websocket.receive_json()
            room_id = data.get("room_id")
            question = data.get("question")
            
            # AI 응답 생성
            response = await create_rag_chain(room_id, question, db)
            
            # 캐시 상태 초기화 및 저장 플래그 추가
            if room_id not in message_cache:
                message_cache[room_id] = {"messages": [], "saved": False}
            
            # 캐시에 질문과 응답 저장
            message_cache[room_id]["messages"].append({"question": question, "response": response})
            print(f"[DEBUG] Message cached for room {room_id}. Cached messages count: {len(message_cache[room_id]['messages'])}")
            
            # 응답을 클라이언트에 JSON 형식으로 전송
            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        print(f"[DEBUG] WebSocket disconnected for room {room_id}.")
        
        # DB 저장 시 플래그 확인
        if room_id and room_id in message_cache and not message_cache[room_id]["saved"]:
            await save_messages_to_db(room_id, message_cache[room_id]["messages"], db)
            
            # 플래그 설정 및 캐시에서 삭제
            message_cache[room_id]["saved"] = True
            message_cache.pop(room_id, None)
            print(f"[DEBUG] Messages saved to DB for room {room_id}. Saved flag set and cache cleared.")
    except Exception as e:
        print(f"WebSocket 처리 중 오류 발생: {e}")

async def save_messages_to_db(room_id, messages, db: AsyncSession):
    """채팅 메시지를 데이터베이스에 저장하는 함수"""
    print(f"[DEBUG] Saving messages to DB for room {room_id}. Messages count: {len(messages)}")
    for msg in messages:
        db_message = ChatMessage(
            room_id=room_id,
            sender_name="User",
            content=msg["question"]
        )
        db.add(db_message)

        ai_response = ChatMessage(
            room_id=room_id,
            sender_name="AI",
            content=msg["response"]
        )
        db.add(ai_response)

    await db.commit()
    print(f"[DEBUG] DB commit complete for room {room_id}.")
