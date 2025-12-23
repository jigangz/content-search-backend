import hashlib
import random
from typing import List, Dict

EMBEDDING_DIM = 1536


def preprocess_text(text: str) -> str:
    """
    Basic text normalization:
    - strip whitespace
    - normalize spaces
    """
    return " ".join(text.strip().split())


def embed_text(text: str) -> List[float]:
    """
    Mock embedding function.
    Deterministic, fixed-dimension (1536), reproducible.

    This simulates real embedding behavior without calling an external model.
    """

    
    hash_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    
    seed = int(hash_digest[:16], 16)
    rng = random.Random(seed)

  
    return [rng.uniform(-1, 1) for _ in range(EMBEDDING_DIM)]


def analyze_text(text: str) -> Dict:
    """
    Core analysis pipeline:
    preprocess → embedding → summary output
    """
    clean_text = preprocess_text(text)
    vector = embed_text(clean_text)

    return {
        "length": len(clean_text),
        "preview": clean_text[:30] + "..." if len(clean_text) > 30 else clean_text,
        "embedding_dim": len(vector),
        
    }


# -----------------------------
# Mock Vector Store 
# -----------------------------

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


def cosine_like(v1: List[float], v2: List[float]) -> float:
    """
    Simple cosine-like similarity (dot product).
    Not normalized — good enough for conceptual understanding.
    """
    return sum(a * b for a, b in zip(v1, v2))


def search_similar(text: str, top_k: int = 1) -> List[Dict]:
    """
    Search most similar documents using vector similarity.
    """
    query_vector = embed_text(preprocess_text(text))

    scored = []
    for doc in VECTOR_STORE:
        score = cosine_like(query_vector, doc["vector"])
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
