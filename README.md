# Drift-Aware LLMOps Monitoring Pipeline

**End-to-end architecture for a monitored Retrieval-Augmented Generation (RAG) system** — detecting retrieval degradation, embedding drift, hallucination spikes, and latency regressions, then triggering corrective actions automatically.
---

## Project Motivation
 
Building a RAG application is only the first step. In real-world AI systems, performance degrades
silently over time — and most teams only discover this after users complain.
 
This project tackles the *post-deployment* problem: **how do you know your RAG system is still working well next week, next month, or after your document corpus changes?**
 
Common causes of silent RAG degradation:
 
| Problem | Signal |
|---|---|
| User query patterns shift | Retrieval distance scores increase over time |
| Documents become outdated | Hit rate drops, answer faithfulness falls |
| Embedding distribution drifts | Centroid shift, KL divergence spikes |
| Index quality degrades | MRR and top-k accuracy decline |
| Answer quality regresses | Hallucination rate or refusal rate increases |
| System under load | P95 latency exceeds acceptable threshold |
 
This project detects all of the above and triggers automated responses — evaluation runs,
alerts, and re-indexing — without human intervention.
---

## Architecture

```text
Knowledge Documents
→ Document Preprocessing & Chunking      (Phase 2: PDF + Markdown with metadata)
→ Embedding Generation                   (sentence-transformers/all-MiniLM-L6-v2)
→ ChromaDB Vector Index
→ FastAPI RAG Endpoint                   (Phase 1: clean service architecture)
→ JSONL Request Logging
→ Evaluation & Drift Monitoring          (Phase 4+5: retrieval metrics + drift detection)
→ Prometheus Metrics Exporter
→ Grafana Dashboard
→ Automated Re-indexing Trigger          (closed-loop maintenance)
```

The system is divided into **6 zones** (see diagram):
 
1. **Knowledge Ingestion & Indexing** — offline batch pipeline, PDF/Markdown → ChromaDB
2. **Online RAG Serving Layer** — FastAPI, query embedding, semantic retrieval, answer generation
3. **Logging & Observability** — every request logged to JSONL with query, answer, distances, latency
4. **Evaluation & Drift Monitoring** — retrieval quality metrics, embedding drift detection, MLflow tracking
5. **Automation & Action Loop** — threshold alerts → re-index trigger → before/after evaluation report
6. **Infrastructure & Delivery** — Docker Compose, GitHub Actions CI/CD


[Architecture Diagram](drift-aware-llmops-monitoring.png)

---

## Tech Stack

| Area | Tools | Version |
|---|---|---|
| Backend API | FastAPI, Uvicorn, Pydantic | `0.111.x` |
| RAG Pipeline | SentenceTransformers, ChromaDB | `2.7.x` / `0.5.x` |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` | — |
| Vector Database | ChromaDB | `0.5.x` |
| Answer Generation | Ollama + Llama 3 (local) | `0.1.x` |
| Document Ingestion | PyMuPDF, Python-Markdown | `1.24.x` |
| Data Processing | Python, Pandas, NumPy | `3.11` |
| Logging | JSONL structured request logs | — |
| Experiment Tracking | MLflow | `2.13.x` |
| Monitoring | Prometheus | `2.51.x` |
| Dashboarding | Grafana | `10.x` |
| Infrastructure | Docker, Docker Compose | — |
| CI/CD | GitHub Actions | — |


---

## Repository Structure

```text
drift-aware-llmops-monitoring/
│
├── app/
│   ├── main.py                    # FastAPI app factory, route registration
│   ├── api/
│   │   └── routes.py              # /query, /health, /metrics endpoints
│   ├── services/
│   │   ├── retrieval.py           # ChromaDB query logic, top-k search
│   │   └── generator.py          # Ollama prompt assembly + answer synthesis
│   ├── schemas/
│   │   └── query.py               # Pydantic request/response models
│   ├── core/
│   │   └── config.py              # Centralized settings (env vars, thresholds)
│   └── logger.py                  # JSONL structured request logger
│
├── indexing/
│   ├── ingest_docs.py             # PDF + Markdown → chunks → embeddings → ChromaDB
│   └── reindex_trigger.py         # Watches metrics, fires re-index when threshold crossed
│
├── monitoring/
│   ├── analyze_logs.py            # Parses JSONL logs, computes aggregate stats
│   ├── drift_detector.py          # Centroid shift + KL divergence on query embeddings
│   ├── retrieval_monitor.py       # Tracks hit rate / MRR degradation over time
│   ├── hallucination_tracker.py   # Flags answers with low context overlap
│   └── prometheus_metrics.py      # Exposes /metrics endpoint for Prometheus scraping
│
├── evaluation/
│   ├── eval_dataset.json          # Ground-truth QA pairs for retrieval evaluation
│   ├── run_eval.py                # Computes hit rate, MRR, top-k accuracy, faithfulness
│   ├── mlflow_tracking.py         # Logs all eval runs to MLflow for comparison
│   └── before_after_report.py     # Generates diff report pre/post re-index
│
├── notebooks/
│   └── drift_analysis_demo.ipynb  # Visual walkthrough: baseline → drift → detection firing
│
├── dashboards/
│   ├── prometheus.yml             # Scrape config
│   └── grafana_dashboard.json     # Pre-built dashboard (import directly into Grafana)
│
├── data/
│   ├── raw_docs/                  # Source documents (PDF, Markdown)
│   └── vector_db/                 # ChromaDB persistent storage
│
├── tests/
│   ├── test_retrieval.py
│   ├── test_drift_detector.py
│   └── test_eval_pipeline.py
│
├── docker-compose.yml             # Spins up: API + ChromaDB + Ollama + Prometheus + Grafana + MLflow
├── Dockerfile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml                 # Lint + test on every push
└── README.md
```


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/trush123ta/drift-aware-llmops-monitoring.git
cd drift-aware-llmops-monitoring
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
**4. Install and start Ollama (local answer generation)**
 
```bash
# Install Ollama: https://ollama.com
ollama pull llama3
ollama serve
```
### 5. Build the Vector Index

```bash
python indexing/ingest_docs.py
```

This creates a local ChromaDB vector database inside:

```text
data/vector_db/
```

### 6. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Query Endpoint

```http
POST /query
```

Example request:

```json
{
  "query": "How do we detect embedding drift?",
  "top_k": 3
}
```

Example response:

```json
{
  "query": "How do we detect embedding drift?",
  "answer": "Based on the retrieved knowledge base, common ways to detect embedding drift include centroid shift, cosine distance distribution changes, nearest-neighbor score degradation, KL divergence, Wasserstein distance, and population stability index.",
  "retrieved_contexts": [
    {
      "text": "Common ways to detect embedding drift include centroid shift, cosine distance distribution changes, nearest-neighbor score degradation, KL divergence, Wasserstein distance, and population stability index.",
      "source": "embedding_drift.md",
      "chunk_index": 1,
      "distance": 0.3674
    }
  ],
  "latency_ms": 14.6,
  "note": "Lower distance means higher semantic similarity."
}
```

---

## Monitoring & Evaluation

Run log analysis:

```bash
python monitoring/analyze_logs.py
```

Run evaluation:

```bash
python evaluation/run_eval.py
```

Start MLflow:

```bash
mlflow ui
```

Start Prometheus and Grafana:

```bash
docker-compose up
```
### Retrieval Quality — Baseline vs. After Re-index
 
| Metric | Baseline | After Re-index | Change |
|---|---|---|---|
| Hit Rate @3 | — | — | — |
| Hit Rate @5 | — | — | — |
| MRR (Mean Reciprocal Rank) | — | — | — |
| Top-3 Accuracy | — | — | — |
| Avg Retrieval Distance | — | — | — |
 
### Answer Quality
 
| Metric | Score | Notes |
|---|---|---|
| Context Faithfulness | — | LLM-judge score 0–1 |
| Answer Correctness | — | vs. ground-truth eval set |
| Hallucination Rate | — | % answers with unsupported claims |
| Refusal Rate | — | % queries with no confident answer |
 
### System Performance
 
| Metric | Value |
|---|---|
| Avg Query Latency | — ms |
| P95 Query Latency | — ms |
| Index Size (chunks) | — |
| Embedding Model | all-MiniLM-L6-v2 |
---

## Metrics Tracked

* Average latency
* Average retrieval distance
* Top-k retrieval accuracy
* Hit rate
* Mean reciprocal rank
* Context precision and recall
* Faithfulness score
* Correctness score
* Hallucination rate
* Refusal rate
* Query embedding drift
* Retrieval degradation alerts

---

## Portfolio Value

This project demonstrates practical AI engineering beyond building a chatbot.
 
It shows hands-on experience with the *production lifecycle* of an AI system:
 
- **RAG system design** — chunking, embedding, semantic retrieval, grounded generation
- **LLMOps** — what happens after deployment, not just during development
- **Observability** — structured logging, Prometheus metrics, Grafana dashboards
- **Evaluation** — quantitative retrieval and answer quality measurement with MLflow tracking
- **Drift detection** — statistical methods for detecting when an embedding-based system degrades
- **Automation** — closed-loop re-indexing triggered by metric thresholds
- **Production mindset** — Docker Compose, CI/CD, modular service architecture

---

## License

This project is intended for educational and portfolio purposes.

---

## Author

**Trusha**

GitHub: [trush123ta](https://github.com/trush123ta)
