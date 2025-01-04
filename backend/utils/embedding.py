from utils.gen_models import GenerationModels
from clients.genai import genai_client


def generate_embedding(text: str, model=GenerationModels.TEXT_EMBEDDING_004):
    response = genai_client.models.embed_content(
        model=model,
        contents=[
            text,
        ],
    )
    return response.embeddings[0].values
