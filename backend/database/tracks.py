from models.audio import Audio
from clients.db import db_client


def create_track(audio: Audio, description: str, embedding: list[float]):
    db_client.table("Tracks").insert(
        {
            "name": audio.title,
            "artists": audio.artists,
            "collection": audio.collection,
            "description": description,
            "embedding": embedding,
        }
    )
