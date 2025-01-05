from typing import Optional

from supabase import Client
from src.clients.db import get_db_client, use_db_client
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
async def embed_retrieve_tracks(
    query_embedding: list[float], db_client: Client, threshold=0.78, count=10
):
    res = await db_client.rpc(
        "get_similar_tracks",
        {
            "query_embedding": query_embedding,
            "match_threshold": threshold,
            "match_count": count,
        },
    ).execute()
    return res.data
