from src.models.message import Message
from src.models.conversation import Conversation
from src.clients.db import db_client


def create_convo() -> Conversation:
    res = db_client.table("Conversations").insert({}).execute()
    data = res.data[0]
    return Conversation(**data)


def get_convo(convo_id: str) -> Conversation:
    res = db_client.table("Conversations").find({"id": convo_id}).execute()
    data = res.data[0]
    return Conversation(**data)


def get_all_convos() -> list[Conversation]:
    res = db_client.table("Conversations").find({}).execute()
    data = res.data
    return [Conversation(**d) for d in data]


def hydrate_history(convo: Conversation) -> Conversation:
    res = db_client.table("Messages").find({"convo_id": convo.id}).execute()
    data = res.data
    convo.history = [Message(**msg) for msg in data]
    return convo


def hydrate_pinned(convo: Conversation) -> Conversation:
    raise NotImplementedError


def hydrate_discarded(convo: Conversation) -> Conversation:
    raise NotImplementedError
