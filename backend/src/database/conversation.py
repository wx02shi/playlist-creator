from typing import Optional

from supabase import Client
from src.clients.db import use_db_client
from src.models.message import Message
from src.models.conversation import Conversation


@use_db_client
def create_convo(db_client: Client) -> Conversation:
    res = db_client.table("Conversations").insert({}).execute()
    data = res.data[0]
    return Conversation(**data)


@use_db_client
def get_convo(convo_id: str, db_client: Client) -> Conversation:
    res = db_client.table("Conversations").find({"id": convo_id}).execute()
    data = res.data[0]
    return Conversation(**data)


@use_db_client
def get_all_convos(db_client: Client) -> list[Conversation]:
    res = db_client.table("Conversations").find({}).execute()
    data = res.data
    return [Conversation(**d) for d in data]


@use_db_client
def hydrate_history(convo: Conversation, db_client: Client) -> Conversation:
    res = db_client.table("Messages").find({"convo_id": convo.id}).execute()
    data = res.data
    convo.history = [Message(**msg) for msg in data]
    return convo


# TODO
@use_db_client
def hydrate_pinned(convo: Conversation, db_client: Client) -> Conversation:
    raise NotImplementedError


@use_db_client
def hydrate_discarded(convo: Conversation, db_client: Client) -> Conversation:
    raise NotImplementedError
