from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from chat import create_rag_chain  

app = FastAPI()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  
    try:
        while True:
            # 클라이언트에서 JSON 형식으로 user_id와 question을 받아 처리
            data = await websocket.receive_json()
            user_id = data.get("user_id")
            question = data.get("question")
            
            # user_id와 question을 사용해 AI 응답 생성
            response = create_rag_chain(user_id, question)
            
            # 응답을 클라이언트에 JSON 형식으로 전송
            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        print("클라이언트와 연결이 끊어졌습니다.")
