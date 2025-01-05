from typing import Optional, Union
from litellm import embedding


def embed_message(
    text: Union[str, list[str]],
    input_type: Optional[str],
    model="embed-multilingual-v3.0",
) -> list[float]:
    print("STARTING EMBEDDING GENERATION...")
    # NOTE: Must pass input_type for Cohere v3 models
    is_batch = isinstance(text, list)
    if not is_batch:
        text = [text]
    if input_type:
        response = embedding(
            model=model,
            input=text,
            input_type=input_type,
        )
    else:
        response = embedding(
            model=model,
            input=text,
        )

    print("EMBEDDING RESPONSE: ", response)

    if is_batch:
        return [r["embedding"] for r in response.data]
    return response.data[0]["embedding"]
