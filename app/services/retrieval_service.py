from typing import Any, Dict, List

import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.services.reranking_service import reranking_service


class RetrievalService:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

    def retrieve(
        self,
        query: str,
        top_k: int,
        use_reranking: bool = True,
        candidate_k: int = 15,
    ) -> List[Dict[str, Any]]:
        query_embedding = self.model.encode([query]).tolist()[0]

        n_results = candidate_k if use_reranking else top_k

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances", "metadatas"],
        )

        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        retrieved_contexts = []

        for doc, distance, metadata in zip(documents, distances, metadatas):
            page = metadata.get("page")

            retrieved_contexts.append(
                {
                    "text": doc,
                    "source": metadata.get("source"),
                    "source_type": metadata.get("source_type"),
                    "page": None if page == -1 else page,
                    "chunk_id": metadata.get("chunk_id"),
                    "chunk_index": metadata.get("chunk_index"),
                    "distance": distance,
                }
            )

        if use_reranking:
            return reranking_service.rerank(
                query=query,
                retrieved_contexts=retrieved_contexts,
                top_k=top_k,
            )

        return retrieved_contexts[:top_k]


retrieval_service = RetrievalService()