from indexing.chunker import chunk_documents
from indexing.document_loader import load_documents
from indexing.embedder import Embedder
from indexing.vector_store import VectorStore


def build_index() -> None:
    documents = load_documents()

    if not documents:
        print("No documents found in data/raw_docs or data/raw_pdfs.")
        return

    chunks = chunk_documents(documents)

    embedder = Embedder()
    embeddings = embedder.embed_texts([chunk["text"] for chunk in chunks])

    vector_store = VectorStore()
    vector_store.clear()
    vector_store.add_chunks(chunks, embeddings)

    print(f"Loaded {len(documents)} documents/pages.")
    print(f"Indexed {len(chunks)} chunks.")


if __name__ == "__main__":
    build_index()