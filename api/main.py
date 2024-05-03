from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()

@app.get("/")
def ping():
    return {"ping": "pong"}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
                try:
                    print("Waiting for message...")
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=5)
                    await websocket.send_text(f"Message text was: {data}")
                except asyncio.TimeoutError:
                    # await websocket.send_text("Timeout!")
                    # print("Timeout!")
                    pass
            #actually will process response.
    except WebSocketDisconnect:
        print("Client disconnected")