def preprocess_text(text: str) -> str:
    return " ".join(text.strip().split())

def embed_text(text: str) -> list[float]:
    """
    Mock embedding function.
    """
    length_feature = float(len(text))
    return [length_feature] * 5

def analyze_text(text: str) -> dict:
    clean_text = preprocess_text(text)

    return {
        "length": len(clean_text),
        "preview": clean_text[:30] + "..." if len(clean_text) > 30 else clean_text,
        "normalized_text": clean_text,
    }


VECTOR_STORE = [
    {
        "id": "doc1",
        "text": "FastAPI is a modern Python web framework",
        "vector": embed_text("FastAPI is a modern Python web framework"),
    },
    {
        "id": "doc2",
        "text": "Embeddings convert text into vectors",
        "vector": embed_text("Embeddings convert text into vectors"),
    },
]

def cosine_like(v1: list[float], v2: list[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))
def search_similar(text: str, top_k: int = 1) -> list[dict]:
    query_vector = embed_text(text)

    scored = []
    for doc in VECTOR_STORE:
        score = cosine_like(query_vector, doc["vector"])
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
