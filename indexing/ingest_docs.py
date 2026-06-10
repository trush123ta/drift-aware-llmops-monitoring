from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Chroma client
client = chromadb.PersistentClient(path="data/vector_db")

collection = client.get_or_create_collection(
    name="knowledge_base"
)

# Read documents
kb_path = Path("data/knowledge_base.txt")

with open(kb_path, "r", encoding="utf-8") as f:
    docs = [line.strip() for line in f.readlines() if line.strip()]

# Generate embeddings
embeddings = model.encode(docs).tolist()

# Clear old collection contents (for development)
existing = collection.get()

if existing["ids"]:
    collection.delete(ids=existing["ids"])

# Add documents
collection.add(
    ids=[str(i) for i in range(len(docs))],
    documents=docs,
    embeddings=embeddings
)

print(f"Indexed {len(docs)} documents.")