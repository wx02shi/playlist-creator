from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    convo_id: str
    role: str
    content: str
    embedding: Optional[list[float]]
    created_at: str
