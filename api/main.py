from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio
import json
import random

load_dotenv()

app = FastAPI()
client = AsyncOpenAI()

conversation_history = []

class MessageQueue:
    def __init__(self):
        self.messages = []
        self.look_from = 0
    
    def add_message(self, message):
        self.messages.append(message)
    
    def get_messages(self):
        if self.look_from >= len(self.messages):
            return []

        messages =  self.messages[self.look_from:]
        self.look_from = len(self.messages)
        return messages

async def reply_to_message(messages):
    
    system_prompt = """You are Bravio a personal human AI. You interact with the user through a chat app where the user may send not only one
                but multiple messages at a time. You are tasked to respond to the user's messages in a friendly manner.
                
                - You will be provided the list of messages sent by the user.
                - You will also answer in a stream of messages rather than a single message. Consider splitting your response into multiple messages when possible.
                - You don't have to reply with the same number of messages as the user sent, keep it varying to make things more realistic.
                - You will communicate just like humans in chat apps, in an informal and friendly manner.
                - You and the user will joke around, have fun, and talk about personal topics.
                - The user can mock you in a friendly way and so can you.
                - You can ask questions to the user to keep the conversation going.
                - You won't help the user with their code.

                Output the following JSON object:
                {
                    "replies" : ["reply1", "reply2", ...]
                }
                
                """
    
    prompt = f"""{{messages: {messages}}}"""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system_prompt}, *conversation_history, {"role": "user", "content": prompt}],
    )

    replies = json.loads(response.choices[0].message.content)
    conversation_history.append({"role": "user", "content": "\n".join(messages)})
    conversation_history.append({"role": "assistant", "content": "\n".join(replies["replies"])})
    return replies["replies"]

    

@app.get("/")
def ping():
    return {"ping": "pong"}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    messages = MessageQueue()
    await websocket.accept()
    print("Client connected")
    try:
        while True:
                try:
                    # print("Waiting for message...")
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=8)
                    messages.add_message(data)
                except asyncio.TimeoutError:
                    messages_to_answer = messages.get_messages()
                    if len(messages_to_answer) > 0:
                        replies = await reply_to_message(messages_to_answer)
                        for reply in replies:
                            await websocket.send_text(reply)
                            #little delay to make it more human like
                            delay = 0.05 * len(reply)
                            await asyncio.sleep(delay)
                        # await websocket.send_text(reply)
                    # await websocket.send_text("Timeout!")
                    # print("Timeout!")
                    pass
            #actually will process response.
    except WebSocketDisconnect:
        print("Client disconnected")