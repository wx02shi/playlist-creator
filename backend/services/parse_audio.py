from database.tracks import create_track
from models.audio import Audio
from clients.db import db_client
from utils.embedding import generate_embedding
from utils.generate import generate_audio_description


def parse_audio(audio: Audio):
    res = generate_audio_description(audio)
    analysis, description = _split_output(res)
    embedding = generate_embedding(description)
    res = create_track(audio, analysis, embedding)
    return res


# HELPERS
def _split_output(output: str):
    # Split on closing analysis tag and extract parts
    analysis_end = output.find("</analysis>") + len("</analysis>")
    analysis = output[:analysis_end]
    description = output[analysis_end:].strip()

    # Extract inner content of analysis tag
    analysis_start = analysis.find("<analysis>") + len("<analysis>")
    analysis = analysis[analysis_start : analysis_end - len("</analysis>")].strip()

    return analysis, description
