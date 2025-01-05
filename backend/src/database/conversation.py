from typing import Optional

from supabase import Client
from src.models.audio import Audio
from src.clients.db import use_db_client
from src.models.message import Message
from src.models.conversation import Conversation


@use_db_client
def create_convo(db_client: Client) -> Conversation:
    res = db_client.table("Conversations").insert({}).execute()
    data = res.data[0]
    return Conversation(**data)


@use_db_client
def update_summary(
    convo: Conversation, new_summary: str, db_client: Client
) -> Conversation:
    res = (
        db_client.table("Conversations")
        .update({"req_summary": new_summary})
        .eq("id", convo.id)
        .execute()
    )
    data = res.data[0]
    return Conversation(**data)


@use_db_client
def get_convo(convo_id: str, db_client: Client) -> Conversation:
    res = db_client.table("Conversations").select("*").eq("id", convo_id).execute()
    data = res.data[0]
    return Conversation(**data)


@use_db_client
def get_all_convos(db_client: Client) -> list[Conversation]:
    res = db_client.table("Conversations").select("*").execute()
    data = res.data
    return [Conversation(**d) for d in data]


@use_db_client
def hydrate_history(convo: Conversation, db_client: Client) -> Conversation:
    res = db_client.table("Messages").select("*").eq("convo_id", convo.id).execute()
    data = res.data
    convo.history = [Message(**msg) for msg in data]
    return convo


@use_db_client
def create_msg(
    content: str,
    convo: Conversation,
    role: str,
    db_client: Client,
    embedding: Optional[list[float]] = None,
) -> Message:
    res = (
        db_client.table("Messages")
        .insert(
            {
                "convo_id": convo.id,
                "role": role,
                "content": content,
                "embedding": embedding,
            }
        )
        .execute()
    )
    data = res.data[0]
    return Message(**data)


@use_db_client
def hydrate_suggested(convo: Conversation, db_client: Client) -> Conversation:
    res = db_client.table("Suggested").select("*").eq("convo_id", convo.id).execute()
    data = res.data
    convo.suggested = [Audio(**a) for a in data]
    return convo


@use_db_client
def hydrate_pinned(convo: Conversation, db_client: Client) -> Conversation:
    res = db_client.table("Pinned").select("*").eq("convo_id", convo.id).execute()
    data = res.data
    convo.pinned = [Audio(**a) for a in data]
    return convo


@use_db_client
def hydrate_discarded(convo: Conversation, db_client: Client) -> Conversation:
    res = db_client.table("Discarded").select("*").eq("convo_id", convo.id).execute()
    data = res.data
    convo.discarded = [Audio(**a) for a in data]
    return convo


@use_db_client
def update_suggested(
    tracks: list[Audio], convo: Conversation, db_client: Client
) -> Conversation:
    res = (
        db_client.table("Suggested")
        .upsert([{"convo_id": convo.id, "track_id": track.id} for track in tracks])
        .execute()
    )
    data = res.data
    convo.suggested = [Audio(**a) for a in data]
    return convo
