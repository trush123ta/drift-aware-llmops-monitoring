from typing import Dict, List

import chromadb

from app.core.config import settings


class VectorStore:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

    def clear(self) -> None:
        existing = self.collection.get()
        if existing["ids"]:
            self.collection.delete(ids=existing["ids"])

    def add_chunks(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
    ) -> None:
        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]

        metadatas = [
            {
                "source": str(chunk["source"]),
                "source_type": str(chunk["source_type"]),
                "page": int(chunk["page"]) if chunk["page"] is not None else -1,
                "chunk_index": int(chunk["chunk_index"]),
                "chunk_id": str(chunk["chunk_id"]),
            }
            for chunk in chunks
        ]
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )