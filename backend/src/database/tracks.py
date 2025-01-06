from typing import Optional

from supabase import Client
from src.clients.db import use_db_client
from src.models.audio import AudioBase


@use_db_client
def create_track(
    audio: AudioBase, description: str, embedding: list[float], db_client: Client
):
    res = (
        db_client.table("Tracks")
        .insert(
            {
                "name": audio.title,
                "artists": audio.artists,
                "collection": audio.collection,
                "description": description,
                "embedding": embedding,
            }
        )
        .execute()
    )
    data = res.data[0]
    return data


@use_db_client
def embed_retrieve_tracks(
    query_embedding: list[float],
    convo_id: str,
    db_client: Client,
    threshold=0.0,
    count=10,
):
    print("RETRIEVING RELEVANT TRACKS")
    res = db_client.rpc(
        "embed_search_v3",
        {
            "query_embedding": query_embedding,
            "match_threshold": threshold,
            "match_count": count,
            "conversation_id": convo_id,
        },
    ).execute()
    print("RETRIEVED RELEVANT TRACKS", res.data)
    return res.data
