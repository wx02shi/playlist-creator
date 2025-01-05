from typing import Optional
from pydantic import BaseModel


class Audio(BaseModel):
    path: str
    title: str
    artists: list[str]
    collection: Optional[str]
