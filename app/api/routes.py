import time

from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.context_service import context_service
from app.services.generation_service import generation_service
from app.services.logging_service import logging_service
from app.services.retrieval_service import retrieval_service


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    start_time = time.time()

    retrieved_contexts = retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k,
    )

    compressed_contexts = context_service.compress_contexts(
        query=request.query,
        retrieved_contexts=retrieved_contexts,
    )

    answer = generation_service.generate_answer(
        query=request.query,
        retrieved_contexts=compressed_contexts,
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    response = {
        "query": request.query,
        "answer": answer,
        "retrieved_contexts": retrieved_contexts,
        "latency_ms": latency_ms,
        "note": "Lower distance means higher semantic similarity. Answer generation uses compressed retrieved context.",
    }

    logging_service.log_request(
        {
            **response,
            "compressed_contexts": compressed_contexts,
        }
    )

    return response