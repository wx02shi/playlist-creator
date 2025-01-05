from src.models.message import Message
from src.database.conversation import get_all_convos, get_convo, hydrate_history


def get_chat_history(convo_id: str) -> list[Message]:
    convo = get_convo(convo_id)
    convo = hydrate_history(convo)
    return convo.history


# TODO: response schemas: attach topic summary and ID
def get_chats():
    convos = get_all_convos()
    return convos
