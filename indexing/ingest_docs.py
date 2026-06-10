from pathlib import Path
from typing import Dict, List

from sentence_transformers import SentenceTransformer
import chromadb


RAW_DOCS_DIR = Path("data/raw_docs")
VECTOR_DB_PATH = "data/vector_db"
COLLECTION_NAME = "knowledge_base"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def read_markdown_files() -> List[Dict]:
    documents = []

    for file_path in RAW_DOCS_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    raw_documents = read_markdown_files()

    all_chunks = []
    all_ids = []
    all_metadata = []

    chunk_id = 0

    for doc in raw_documents:
        chunks = chunk_text(doc["text"])

        for chunk_index, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(str(chunk_id))
            all_metadata.append(
                {
                    "source": doc["source"],
                    "chunk_index": chunk_index,
                }
            )
            chunk_id += 1

    embeddings = model.encode(all_chunks).tolist()

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadata,
    )

    print(f"Indexed {len(all_chunks)} chunks from {len(raw_documents)} documents.")


if __name__ == "__main__":
    build_index()