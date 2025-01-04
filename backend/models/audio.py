from pydantic import BaseModel


class Audio(BaseModel):
    path: str
    title: str
    artists: list[str]
    collection: str
