from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class RetrievalService:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        query_embedding = self.model.encode([query]).tolist()[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "distances", "metadatas"],
        )

        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        retrieved_contexts = []

        for doc, distance, metadata in zip(documents, distances, metadatas):
            retrieved_contexts.append(
                {
                    "text": doc,
                    "source": metadata.get("source"),
                    "source_type": metadata.get("source_type"),
                    "page": metadata.get("page"),
                    "chunk_id": metadata.get("chunk_id"),
                    "chunk_index": metadata.get("chunk_index"),
                    "distance": distance,
                }
            )

        return retrieved_contexts


retrieval_service = RetrievalService()