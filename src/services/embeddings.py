from sentence_transformers import SentenceTransformer
import numpy as np

_model = None


def get_model():
    global _model
    if _model is None:
        print("Loading embedding model (first time)...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
    return _model


def embed_texts(texts: list) -> list:

    if not texts:
        return []
    
    model = get_model()
    embeddings = model.encode(texts)
    
    return embeddings.tolist()


def embed_query(text: str) -> list:
    return embed_texts([text])[0]