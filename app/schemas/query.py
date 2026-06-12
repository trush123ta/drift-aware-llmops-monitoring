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


class QueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_contexts: List[RetrievedContext]
    latency_ms: float
    note: str