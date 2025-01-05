from typing import Optional, Tuple
from src.clients.retrieval import embed_message
from src.database.tracks import embed_retrieve_tracks
from src.schemas.responses import ChatResponse, ConversationBaseResponse
from src.clients.db import get_db_client
from src.clients.llm import helper_agent_completion
from src.database.conversation import *
from src.utils.prompts import (
    summarize_requirements,
    update_requirements_summary,
    inject_pinned,
    compare_summaries,
)
from src.utils.temp_embed import temp
from src.utils.parse_str_embed import embed_str_to_list


def create_chat() -> ConversationBaseResponse:
    db_client = get_db_client()
    convo = create_convo(db_client=db_client)
    res = ConversationBaseResponse(**convo.model_dump())
    return res


async def chat(msg: str, convo_id: str) -> ChatResponse:
    print("chatting\n\n\n\n\n\n")
    db_client = get_db_client()
    convo, is_first_msg = _init_convo(convo_id, db_client=db_client)

    new_req_summary = _summarize_reqs(msg, convo, is_first_msg)

    if convo.pinned and len(convo.pinned) > 0:
        new_req_summary = _inject_pinned_desc(convo, new_req_summary)

    # summary_embedding = embed_message(new_req_summary, input_type="search_query")
    summary_embedding = temp
    retrieved_tracks = _retrieve_tracks(summary_embedding, db_client=db_client)

    print(len(retrieved_tracks))

    chat_response = _compare_summaries(msg, convo.req_summary, new_req_summary)

    convo, chat_msg = _update_convo(
        convo,
        msg,
        new_req_summary,
        summary_embedding,
        chat_response,
        retrieved_tracks,
        db_client=db_client,
    )

    res = ChatResponse(**chat_msg.model_dump())
    return res


# HELPERS
def _init_convo(convo_id: Optional[str], db_client) -> Tuple[Conversation, bool]:
    convo = get_convo(convo_id, db_client=db_client)
    convo = hydrate_history(convo, db_client=db_client)
    is_first_msg = len(convo.history) == 0

    convo = hydrate_suggested(convo, db_client=db_client)
    convo = hydrate_pinned(convo, db_client=db_client)
    convo = hydrate_discarded(convo, db_client=db_client)

    return convo, is_first_msg


def _summarize_reqs(msg: str, convo: Conversation, is_first_msg: bool) -> str:
    if is_first_msg:
        instructions = summarize_requirements
    else:
        instructions = update_requirements_summary.format(summary=convo.req_summary)

    req_summary = helper_agent_completion(instructions, msg)
    return req_summary


def _inject_pinned_desc(convo: Conversation, req_summary: str) -> str:
    assert convo.pinned
    pinned = [
        {
            "title": a.title,
            "artists": a.artists,
            "collection": a.collection,
            "description": a.description,
        }
        for a in convo.pinned
    ]
    pinned_summary = helper_agent_completion(inject_pinned, pinned)
    req_summary += (
        "\nThe following is a description of tracks the user has pinned. These are a stronger indication of their preference:\n"
        + pinned_summary
    )
    return req_summary


def _retrieve_tracks(summary_embedding: list[float], db_client: Client) -> list[Audio]:
    retrieved_tracks = embed_retrieve_tracks(summary_embedding, db_client=db_client)
    res = [
        Audio(
            id=track["id"],
            title=track["name"],
            artists=track["artists"],
            collection=track["collection"],
            description=track["description"],
            embedding=embed_str_to_list(track["embedding"]),
        )
        for track in retrieved_tracks
    ]
    return res


def _compare_summaries(msg: str, old_summary: str, new_summary: str) -> str:
    instructions = compare_summaries.format(latest_request=msg)
    summaries = f"<old_summary>\n{old_summary}\n</old_summary>\n<new_summary>\n{new_summary}\n</new_summary>"
    response = helper_agent_completion(instructions, summaries)
    return response


def _update_convo(
    convo: Conversation,
    user_query: str,
    new_req_summary: str,
    new_req_summary_embedding: list[float],
    chat_response: str,
    retrieved_tracks: list[Audio],
    db_client: Client,
) -> Tuple[Conversation, Message]:
    # update latest summary
    convo = update_summary(convo, new_req_summary, db_client=db_client)

    # update message history
    user_msg = create_msg(
        user_query,
        convo,
        role="user",
        db_client=db_client,
    )
    assistant_msg = create_msg(
        chat_response,
        convo,
        role="assistant",
        db_client=db_client,
        embedding=new_req_summary_embedding,
    )
    convo = hydrate_history(convo, db_client=db_client)

    # update tracks
    convo = update_suggested(retrieved_tracks, convo, db_client=db_client)

    return convo, assistant_msg
