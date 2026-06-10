from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import retrieve_documents

app = FastAPI(title="Drift-Aware LLMOps Monitoring Pipeline")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@app.get("/")
def health_check():
    return {"status": "ok", "message": "LLMOps monitoring pipeline is running"}


@app.post("/query")
def query_rag(request: QueryRequest):
    docs, distances = retrieve_documents(request.query, request.top_k)

    return {
        "query": request.query,
        "retrieved_docs": docs,
        "retrieval_distances": distances,
        "note": "Lower distance means higher semantic similarity."
    }