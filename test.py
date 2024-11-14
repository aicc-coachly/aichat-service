import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:6666/ws/chat"  # WebSocket 엔드포인트
    try:
        async with websockets.connect(uri) as websocket:
            # WebSocket에 메시지 전송
            message = {"user_id": 28, "question": "Hello, AI!"}
            await websocket.send(json.dumps(message))
            print("Sent:", message)

            # 서버로부터 응답 받기
            response = await websocket.recv()
            print("Received:", response)

    except websockets.ConnectionClosedError:
        print("Connection was closed unexpectedly. Retrying...")

    except Exception as e:
        print(f"An error occurred: {e}")

# asyncio.run을 try-except 블록 안에 넣어 재시도를 가능하게 함
if __name__ == "__main__":
    try:
        asyncio.run(test_websocket())
    except Exception as e:
        print(f"Failed to run WebSocket test: {e}")
