from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import settings


class Embedder:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()