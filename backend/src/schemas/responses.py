from typing import Optional
from pydantic import BaseModel


class ChatResponse(BaseModel):
    id: int
    convo_id: str
    role: str
    content: str
    created_at: str


class ChatHistoryResponse(BaseModel):
    convo_id: str
    history: list[ChatResponse]


class ConversationBaseResponse(BaseModel):
    id: str
    req_summary: Optional[str]


class AllConversationsResponse(BaseModel):
    conversations: list[ConversationBaseResponse]
