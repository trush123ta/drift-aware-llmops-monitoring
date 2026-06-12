import time

from fastapi import APIRouter

from app.schemas.query import QueryRequest, QueryResponse
from app.services.context_service import context_service
from app.services.generation_service import generation_service
from app.services.logging_service import logging_service
from app.services.retrieval_service import retrieval_service
from app.services.source_service import source_service


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    total_start_time = time.time()

    retrieval_start_time = time.time()
    retrieved_contexts = retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k,
    )
    retrieval_latency_ms = round((time.time() - retrieval_start_time) * 1000, 2)

    top_contexts_for_generation = retrieved_contexts[:1]

    compressed_contexts = context_service.compress_contexts(
        query=request.query,
        retrieved_contexts=top_contexts_for_generation,
    )

    generation_start_time = time.time()
    answer = generation_service.generate_answer(
        query=request.query,
        retrieved_contexts=compressed_contexts,
    )
    generation_latency_ms = round((time.time() - generation_start_time) * 1000, 2)

    total_latency_ms = round((time.time() - total_start_time) * 1000, 2)

    sources = source_service.build_sources(retrieved_contexts)

    response = {
        "query": request.query,
        "answer": answer,
        "sources": sources,
        "retrieved_contexts": retrieved_contexts,
        "retrieval_latency_ms": retrieval_latency_ms,
        "generation_latency_ms": generation_latency_ms,
        "total_latency_ms": total_latency_ms,
        "note": "Lower distance means higher semantic similarity. Answer generation uses compressed retrieved context.",
    }

    logging_service.log_request(
        {
            **response,
            "compressed_contexts": compressed_contexts,
        }
    )

    return response