from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from chat import create_rag_chain  # AI 응답 생성 함수
from database import get_db  # 데이터베이스 연결 가져오기
from model import ChatMessage

app = FastAPI()

# 사용자 메시지 캐시용 딕셔너리
message_cache = {}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    user_id = None
    try:
        while True:
            # 클라이언트에서 JSON 형식으로 user_id와 question을 받아 처리
            data = await websocket.receive_json()
            user_id = data.get("user_id")
            question = data.get("question")
            
            # AI 응답 생성
            response = create_rag_chain(user_id, question)
            
            # 응답을 캐시에 추가
            if user_id not in message_cache:
                message_cache[user_id] = []
            message_cache[user_id].append({"question": question, "response": response})
            
            # 응답을 클라이언트에 JSON 형식으로 전송
            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        print(f"{user_id}와의 연결이 끊어졌습니다.")
        # 연결이 끊어지면 캐시된 메시지를 데이터베이스에 저장
        if user_id and user_id in message_cache:
            await save_messages_to_db(user_id, message_cache[user_id], db)
            # 저장 후 캐시에서 해당 메시지 삭제
            del message_cache[user_id]

async def save_messages_to_db(user_id, messages, db: AsyncSession):
    """채팅 메시지를 데이터베이스에 저장하는 함수"""
    for msg in messages:
        db_message = ChatMessage(
            user_id=user_id,
            question=msg["question"],
            response=msg["response"]
        )
        db.add(db_message)
    await db.commit()
