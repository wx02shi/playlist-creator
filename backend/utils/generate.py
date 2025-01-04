import os

from google import genai
from google.genai import types

from models.audio import Audio
from utils.gen_models import GenerationModels
from utils.prompts import description_prompt, track_details
from clients.genai import genai_client


def generate_audio_description(
    audio: Audio, model=GenerationModels.GEMINI_2_0_FLASH_EXP
):
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


def _format_track_details(audio: Audio):
    title = audio.title
    artists = audio.artists
    collection_title = audio.collection

    return track_details.format(
        title=title, artists=artists, collection_title=collection_title
    )


def _create_audio_part(audio: Audio):
    filename = audio.path

    with open(filename, "rb") as f:
        data = f.read()
    return types.Part.from_bytes(data=data, mime_type="audio/mp3")
