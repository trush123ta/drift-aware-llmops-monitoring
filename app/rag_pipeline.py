from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="data/vector_db")
collection = client.get_or_create_collection(name="knowledge_base")


def retrieve_documents(query: str, top_k: int = 3):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    return documents, distances