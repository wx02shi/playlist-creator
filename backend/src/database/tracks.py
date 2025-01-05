from src.models.audio import Audio
from src.clients.db import db_client


def create_track(audio: Audio, description: str, embedding: list[float]):
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
