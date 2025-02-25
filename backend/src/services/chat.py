import json
from typing import Optional, Tuple
from src.clients.retrieval import embed_message, rerank_query
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
from src.utils.parse_str_embed import embed_str_to_list
from src.utils.temp_embed import temp


def create_chat() -> ConversationBaseResponse:
    db_client = get_db_client()
    convo = create_convo(db_client=db_client)
    res = ConversationBaseResponse(**convo.model_dump())
    return res


async def chat(msg: str, convo_id: str) -> ChatResponse:
    print("chatting...")
    db_client = get_db_client()
    convo, is_first_msg = _init_convo(convo_id, db_client=db_client)

    new_req_summary = _summarize_reqs(msg, convo, is_first_msg)

    if convo.pinned and len(convo.pinned) > 0:
        new_req_summary = _inject_pinned_desc(convo, new_req_summary)
    print("new_req_summary: ", new_req_summary)

    # TODO: re-enable Cohere calls when finalized
    summary_embedding = embed_message(new_req_summary, input_type="search_query")
    # summary_embedding = temp
    retrieved_tracks = _retrieve_tracks(convo, summary_embedding, db_client=db_client)
    reranked_tracks = _rerank_tracks(new_req_summary, retrieved_tracks)
    # reranked_tracks = retrieved_tracks

    chat_response = _compare_summaries(msg, convo.req_summary, new_req_summary)

    convo, chat_msg = _update_convo(
        convo,
        msg,
        new_req_summary,
        summary_embedding,
        chat_response,
        reranked_tracks,
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
    formatted_pinned = "<pinned_tracks>\n[\n"
    for track in pinned:
        formatted_pinned += json.dumps(track, indent=4) + ",\n"
    formatted_pinned += "]\n</pinned_tracks>"
    pinned_summary = helper_agent_completion(inject_pinned, formatted_pinned)
    print(formatted_pinned)
    req_summary += (
        "\nThe following is a description of tracks the user has pinned. These are a stronger indication of their preference:\n"
        + pinned_summary
    )
    return req_summary


def _retrieve_tracks(
    convo: Conversation, summary_embedding: list[float], db_client: Client
) -> list[Audio]:
    retrieved_tracks = embed_retrieve_tracks(
        summary_embedding, convo.id, db_client=db_client
    )
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


def _rerank_tracks(summary: str, retrieved_tracks: list[Audio]) -> list[Audio]:
    descriptions = [track.description for track in retrieved_tracks]
    results = rerank_query(summary, descriptions)
    reranked_tracks = [retrieved_tracks[result["index"]] for result in results]
    return reranked_tracks


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


def get_history(convo_id: str):
    db_client = get_db_client()
    convo = get_convo(convo_id, db_client=db_client)
    convo = hydrate_history(convo, db_client=db_client)
    res = [Message(**msg.model_dump()) for msg in convo.history]
    return res


def get_tracks(convo_id: str):
    db_client = get_db_client()
    convo = get_convo(convo_id, db_client=db_client)
    convo = hydrate_suggested(convo, db_client=db_client)
    convo = hydrate_pinned(convo, db_client=db_client)
    res = {
        "suggested": [
            {
                "title": track.title,
                "artists": track.artists,
                "collection": track.collection,
                "description": track.description,
                "id": track.id,
            }
            for track in convo.suggested
        ],
        "pinned": [
            {
                "title": track.title,
                "artists": track.artists,
                "collection": track.collection,
                "description": track.description,
                "id": track.id,
            }
            for track in convo.pinned
        ],
    }
    return res


def get_all_chats():
    db_client = get_db_client()
    convos = get_all_convos(db_client=db_client)
    res = [ConversationBaseResponse(**convo.model_dump()) for convo in convos]
    res = {
        "conversations": res,
    }
    return res
