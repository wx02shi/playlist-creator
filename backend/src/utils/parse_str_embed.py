def embed_str_to_list(embed_str: str) -> list[float]:
    return [float(x) for x in embed_str.strip("[]").split(",")]
