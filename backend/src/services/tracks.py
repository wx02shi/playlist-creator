from src.database.conversation import remove_suggested
from src.database.tracks import pin_track_db
from src.clients.db import get_db_client


def pin_track(convoId: str, trackId: int):
    db_client = get_db_client()
    res = pin_track_db(convoId, trackId, db_client=db_client)
    remove_suggested(trackId, convoId, db_client=db_client)
    return res
