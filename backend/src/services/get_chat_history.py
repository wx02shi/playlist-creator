from src.schemas.responses import ChatHistoryResponse
from src.database.conversation import get_all_convos, get_convo, hydrate_history


def get_chat_history(convo_id: str) -> ChatHistoryResponse:
    convo = get_convo(convo_id)
    convo = hydrate_history(convo)
    res = ChatHistoryResponse(
        convo_id=convo.id, history=[msg.dict() for msg in convo.history]
    )
    return res


# TODO: response schemas: attach topic summary and ID
def get_chats():
    convos = get_all_convos()
    return convos
