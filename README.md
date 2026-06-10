# Drift-Aware LLMOps Monitoring Pipeline

A portfolio project demonstrating how to monitor a Retrieval-Augmented Generation (RAG) system after deployment.

## Current Features

- FastAPI-based RAG API
- Semantic retrieval using SentenceTransformers
- ChromaDB vector database
- Request logging in JSONL format
- Retrieval distance tracking
- Latency tracking
- Basic monitoring summary script

## Current Pipeline

```text
User Query
→ FastAPI Endpoint
→ Query Embedding
→ ChromaDB Vector Search
→ Top-k Document Retrieval
→ Latency + Retrieval Distance Logging
→ Monitoring Summary