import time

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import retrieve_documents
from app.logger import log_rag_request


app = FastAPI(title="Drift-Aware LLMOps Monitoring Pipeline")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@app.get("/")
def health_check():
    return {"status": "ok", "message": "LLMOps monitoring pipeline is running"}


@app.post("/query")
def query_rag(request: QueryRequest):
    start_time = time.time()

    docs, distances = retrieve_documents(request.query, request.top_k)

    latency_ms = round((time.time() - start_time) * 1000, 2)

    response = {
        "query": request.query,
        "retrieved_docs": docs,
        "retrieval_distances": distances,
        "latency_ms": latency_ms,
        "note": "Lower distance means higher semantic similarity."
    }

    log_rag_request(response.copy())

    return response