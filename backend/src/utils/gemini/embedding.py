import os
from google import genai
from src.utils.gemini.gen_models import GenerationModels


def generate_embedding(text: str, model=GenerationModels.TEXT_EMBEDDING_004):
    genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = genai_client.models.embed_content(
        model=model,
        contents=[
            text,
        ],
    )
    return response.embeddings[0].values
