from typing import Optional, Union
from litellm import embedding, rerank


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


def rerank_query(
    query: str, documents: list[str], top_n: int = 5, model="cohere/rerank-english-v3.0"
):
    print("STARTING RERANKING ...")
    res = rerank(model=model, query=query, documents=documents, top_n=top_n)
    print("RERANKING RESPONSE: ", res)
    return res.results
