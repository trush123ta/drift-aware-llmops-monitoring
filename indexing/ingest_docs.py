import json
from collections import Counter
from datetime import datetime, timezone

from app.core.config import settings
from indexing.chunker import chunk_documents
from indexing.document_loader import load_documents
from indexing.embedder import Embedder
from indexing.vector_store import VectorStore


def save_ingestion_report(documents, chunks) -> None:
    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    source_counter = Counter(chunk["source"] for chunk in chunks)
    source_type_counter = Counter(chunk["source_type"] for chunk in chunks)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "loaded_documents_or_pages": len(documents),
        "indexed_chunks": len(chunks),
        "chunks_by_source_type": dict(source_type_counter),
        "chunks_by_source": dict(source_counter),
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "chunk_size": settings.CHUNK_SIZE,
        "vector_db_path": settings.VECTOR_DB_PATH,
        "collection_name": settings.COLLECTION_NAME,
    }

    report_path = settings.PROCESSED_DIR / "ingestion_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    chunks_path = settings.PROCESSED_DIR / "indexed_chunks_preview.json"

    preview = [
        {
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "source_type": chunk["source_type"],
            "page": chunk["page"],
            "chunk_index": chunk["chunk_index"],
            "text_preview": chunk["text"][:300],
        }
        for chunk in chunks
    ]

    with open(chunks_path, "w", encoding="utf-8") as file:
        json.dump(preview, file, indent=2)


def build_index() -> None:
    documents = load_documents()

    if not documents:
        print("No documents found in data/raw_docs or data/raw_pdfs.")
        return

    chunks = chunk_documents(documents)

    if not chunks:
        print("No valid chunks found after cleaning/filtering.")
        return

    embedder = Embedder()
    embeddings = embedder.embed_texts([chunk["text"] for chunk in chunks])

    vector_store = VectorStore()
    vector_store.clear()
    vector_store.add_chunks(chunks, embeddings)

    save_ingestion_report(documents, chunks)

    print(f"Loaded {len(documents)} documents/pages.")
    print(f"Indexed {len(chunks)} chunks.")
    print("Saved ingestion report to data/processed/ingestion_report.json")
    print("Saved chunk preview to data/processed/indexed_chunks_preview.json")


if __name__ == "__main__":
    build_index()