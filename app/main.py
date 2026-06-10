from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import retrieve_documents

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/query")
def query_rag(request: QueryRequest):

    docs = retrieve_documents(request.query)

    return {
        "query": request.query,
        "retrieved_docs": docs
    }