from dotenv import load_dotenv
from fastapi import FastAPI
from src.schemas.requests import ChatRequest
from src.services.chat import (
    chat as chat_service,
    create_chat as create_chat_service,
    get_history as get_history_service,
    get_tracks as get_tracks_service,
    get_all_chats as get_all_chats_service,
)
from src.services.tracks import pin_track as pin_track_service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return "Healthy"


@app.put("/chat/create")
def create_chat():
    return create_chat_service()


@app.post("/chat/{convoId}")
async def chat(convoId: str, msg_req: ChatRequest):
    return await chat_service(msg_req.content, convoId)


@app.get("/chat/{convoId}/tracks")
def get_tracks(convoId: str):
    return get_tracks_service(convoId)


@app.get("/chat/{convoId}")
def get_history(convoId: str):
    return get_history_service(convoId)


@app.get("/all-chats")
def get_all_chats():
    return get_all_chats_service()


@app.put("/pin/{convoId}/{trackId}")
def pin_track(convoId: str, trackId: str):
    return pin_track_service(convoId, trackId)
