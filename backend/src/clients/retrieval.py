from typing import Optional, Union
from litellm import embedding


def embed_message(
    text: Union[str, list[str]], input_type: Optional[str], model="embed-english-v3.0"
):
    # NOTE: Must pass input_type for Cohere v3 models
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

    return response
