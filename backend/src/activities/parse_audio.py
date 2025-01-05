from src.database.tracks import create_track
from src.models.audio import AudioBase
from src.utils.gemini.embedding import generate_embedding
from src.utils.gemini.generate import generate_audio_description

from temporalio import activity


@activity.defn
async def parse_audio(audio: AudioBase):
    res = generate_audio_description(audio)
    _, description = _split_output(res)
    embedding = generate_embedding(description)
    res = create_track(audio, res, embedding)
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
