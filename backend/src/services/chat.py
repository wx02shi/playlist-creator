from typing import Optional
from database.conversation import *


def chat(msg: str, convo_id: Optional[str]) -> Message:
    if not convo_id:
        convo = create_convo()
    else:
        convo = get_convo(convo_id)

    # Create an updated summary of the user's requirements

    # Retrieve pinned tracks
    # Create a summary of the pinned tracks
    # Update the summary of the user's requirements

    # Retrieve tracks

    # Create a chat response summary of the results
    # If the summary was updated, create a comparison of the last chat response and the new chat response, and return that instead

    res = None

    return res
