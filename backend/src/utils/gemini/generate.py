import os

from google import genai
from google.genai import types

from src.models.audio import AudioBase
from src.utils.gemini.gen_models import GenerationModels
from src.utils.prompts import description_prompt, track_details


def generate_audio_description(
    audio: AudioBase, model=GenerationModels.GEMINI_2_0_FLASH_EXP
):
    genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    config = _get_config()
    formatted_details = _format_track_details(audio)
    audio_part = _create_audio_part(audio)

    response = genai_client.models.generate_content(
        model=model,
        config=config,
        contents=[formatted_details, audio_part],
    )
    return response.text


# HELPERS
def _get_config():
    return types.GenerateContentConfig(
        system_instruction=description_prompt,
    )


def _format_track_details(audio: AudioBase):
    title = audio.title
    artists = audio.artists
    collection_title = ""
    if audio.collection:
        collection_title = audio.collection

    return track_details.format(
        title=title, artists=artists, collection_title=collection_title
    )


def _create_audio_part(audio: AudioBase):
    filename = audio.path

    with open(filename, "rb") as f:
        data = f.read()
    return types.Part.from_bytes(data=data, mime_type="audio/mp3")
