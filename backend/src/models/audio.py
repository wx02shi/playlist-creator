from typing import Optional
from pydantic import BaseModel


class AudioBase(BaseModel):
    path: Optional[str] = None
    title: str
    artists: list[str]
    collection: Optional[str]


class Audio(AudioBase):
    id: int
    description: str
    embedding: list[float]
