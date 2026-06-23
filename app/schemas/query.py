from typing import List

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


class RetrievedContext(BaseModel):
    text: str
    source: str | None = None
    source_type: str | None = None
    page: int | None = None
    chunk_id: str | None = None
    chunk_index: int | None = None
    distance: float
    rerank_score: float | None = None
    keyword_overlap: int | None = None


class SourceCitation(BaseModel):
    source_id: str
    source: str | None = None
    source_type: str | None = None
    page: int | None = None
    chunk_id: str | None = None
    distance: float


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceCitation]
    retrieved_contexts: List[RetrievedContext]
    retrieval_latency_ms: float
    generation_latency_ms: float
    total_latency_ms: float
    note: str