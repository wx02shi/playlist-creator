from typing import Optional, Tuple
from clients.retrieval import embed_message
from database.tracks import embed_retrieve_tracks
from src.clients.db import get_db_client
from src.clients.llm import helper_agent_completion
from src.database.conversation import *
from src.utils.prompts import (
    summarize_requirements,
    update_requirements_summary,
    inject_pinned,
)


async def chat(msg: str, convo_id: Optional[str]) -> Tuple[Conversation, Message]:
    db_client = get_db_client()
    convo, is_first_msg = _init_convo(convo_id, db_client=db_client)

    new_req_summary = _summarize_reqs(msg, convo, is_first_msg)

    if convo.pinned and len(convo.pinned) > 0:
        new_req_summary = _inject_pinned_desc(convo, new_req_summary)

    summary_embedding = embed_message(new_req_summary, input_type="search_query")

    retrieved_tracks = embed_retrieve_tracks(summary_embedding, db_client=db_client)

    # If the summary was updated, create a comparison of the last chat response and the new chat response, and return that instead

    res = None

    return res


def _init_convo(convo_id: Optional[str], db_client) -> Tuple[Conversation, bool]:
    is_first_msg = convo_id is None
    if is_first_msg:
        convo = create_convo(db_client)
    else:
        convo = get_convo(db_client, convo_id)

    convo = hydrate_history(db_client, convo)
    convo = hydrate_pinned(db_client, convo)
    convo = hydrate_discarded(db_client, convo)

    return convo, is_first_msg


def _summarize_reqs(msg: str, convo: Conversation, is_first_msg: bool) -> str:
    if is_first_msg:
        instructions = summarize_requirements
    else:
        instructions = update_requirements_summary.format(summary=convo.req_summary)

    req_summary = helper_agent_completion(instructions, msg)
    return req_summary


def _inject_pinned_desc(convo: Conversation, req_summary) -> str:
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
