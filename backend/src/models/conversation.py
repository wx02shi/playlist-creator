from typing import Optional
from pydantic import BaseModel

from src.models.audio import Audio
from src.models.message import Message


class Conversation(BaseModel):
    id: str
    req_summary: Optional[str] = None
    res_summary: Optional[str] = None
    topic_summary: Optional[str] = None
    # Optional for the purpose of run-time hydration
    pinned: Optional[list[Audio]] = None
    discarded: Optional[list[Audio]] = None
    history: Optional[list[Message]] = None
