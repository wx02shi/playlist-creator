import sys
from dotenv import load_dotenv

sys.path.append("..")
from src.clients.retrieval import embed_message
from src.clients.db import get_db_client
from src.utils.temp_embed import temp


def _split_output(output: str):
    # Split on closing analysis tag and extract parts
    analysis_end = output.find("</analysis>") + len("</analysis>")
    analysis = output[:analysis_end]
    description = output[analysis_end:].strip()

    # Extract inner content of analysis tag
    analysis_start = analysis.find("<analysis>") + len("<analysis>")
    analysis = analysis[analysis_start : analysis_end - len("</analysis>")].strip()

    return analysis, description


def migrate():
    load_dotenv()

    db_client = get_db_client()
    # retrieve all tracks
    res = db_client.table("Tracks").select("*").execute()
    tracks = res.data
    full_descriptions = [track["description"] for track in tracks]

    # split the descriptions again
    descriptions = [_split_output(description)[1] for description in full_descriptions]

    print(len(descriptions))
    # print(tracks[0])
    # obtain new embeddings for all tracks
    embed_res = embed_message(descriptions, input_type="search_document")

    # create replicas in different table, with the new embeddings
    inserts = [
        {
            "name": track["name"],
            "artists": track["artists"],
            "collection": track["collection"],
            "description": track["description"],
            "embedding": embedding,
        }
        for track, embedding in zip(tracks, embed_res)
    ]

    print(inserts[0])

    res = db_client.table("NewTracks").insert(inserts).execute()
    print(res)


if __name__ == "__main__":
    migrate()
