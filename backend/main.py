from dotenv import load_dotenv
from fastapi import FastAPI
from src.schemas.requests import ChatRequest
from src.services.chat import chat as chat_service, create_chat as create_chat_service

app = FastAPI()
load_dotenv()


@app.get("/")
def health():
    return "Healthy"


@app.put("/chat/create")
def create_chat():
    return create_chat_service()


@app.post("/chat/{convoId}")
async def chat(convoId: str, msg_req: ChatRequest):
    return await chat_service(msg_req.content, convoId)
