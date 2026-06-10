# Drift-Aware LLMOps Monitoring Pipeline

A portfolio project demonstrating how to monitor, evaluate, and maintain a Retrieval-Augmented Generation (RAG) system after deployment.

This project focuses on **LLMOps**, **RAG monitoring**, **embedding drift detection**, **retrieval quality tracking**, and **automated re-indexing triggers**. The goal is to show how an AI system can be continuously observed and improved after it is deployed.

---

## Project Motivation

Building a RAG application is only the first step. In real-world AI systems, performance can degrade over time due to:

* Changes in user query patterns
* Outdated documents
* Embedding distribution drift
* Retrieval degradation
* Hallucination spikes
* Increased refusal or fallback responses
* Latency issues
* Poor indexing quality

This project demonstrates how to detect these issues and prepare automated responses such as evaluation runs, alerts, and re-indexing triggers.

---

## Architecture

```text
Knowledge Documents
→ Document Preprocessing & Chunking
→ Embedding Generation
→ ChromaDB Vector Index
→ FastAPI RAG Endpoint
→ Request Logging
→ Evaluation & Drift Monitoring
→ Prometheus Metrics
→ Grafana Dashboard
→ Re-indexing / Retraining Trigger
```

![Architecture Diagram](drift-aware-llmops-monitoring.png)

---

## Tech Stack

| Area                | Tools                                           |
| ------------------- | ----------------------------------------------- |
| Backend API         | FastAPI, Uvicorn, Pydantic                      |
| RAG Pipeline        | SentenceTransformers, ChromaDB                  |
| Embedding Model     | `sentence-transformers/all-MiniLM-L6-v2`        |
| Vector Database     | ChromaDB                                        |
| Data Processing     | Python, Pandas, NumPy                           |
| Logging             | JSONL request logs                              |
| Evaluation          | Custom retrieval metrics, answer-quality checks |
| Experiment Tracking | MLflow                                          |
| Monitoring          | Prometheus                                      |
| Dashboarding        | Grafana                                         |
| Automation          | Threshold rules, re-indexing trigger            |
| DevOps              | Docker, Docker Compose, GitHub Actions          |
| Version Control     | Git, GitHub                                     |

---

## Repository Structure

```text
drift-aware-llmops-monitoring/
│
├── app/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── generator.py
│   └── logger.py
│
├── indexing/
│   ├── ingest_docs.py
│   └── reindex_trigger.py
│
├── monitoring/
│   ├── analyze_logs.py
│   ├── drift_detector.py
│   ├── retrieval_monitor.py
│   ├── hallucination_tracker.py
│   └── prometheus_metrics.py
│
├── evaluation/
│   ├── eval_dataset.json
│   ├── run_eval.py
│   ├── mlflow_tracking.py
│   └── before_after_report.py
│
├── dashboards/
│   ├── prometheus.yml
│   └── grafana_dashboard.json
│
├── data/
│   ├── raw_docs/
│   └── vector_db/
│
├── tests/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Current Implementation

The current implementation includes the core RAG and monitoring foundation:

* FastAPI `/query` endpoint
* Semantic retrieval with SentenceTransformers
* ChromaDB vector indexing
* Markdown document ingestion
* Paragraph-aware chunking
* Source and chunk metadata tracking
* Retrieval distance reporting
* Latency measurement
* JSONL request logging
* Basic monitoring summary script
* Basic grounded answer generation

---

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

If activation is blocked:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Build the Vector Index

```bash
python indexing/ingest_docs.py
```

This creates a local ChromaDB vector database inside:

```text
data/vector_db/
```

### 5. Run the FastAPI Server

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

This project demonstrates practical AI engineering skills beyond basic model usage.

It shows experience with:

* RAG system design
* Semantic search
* Vector databases
* Embedding models
* LLMOps monitoring
* Retrieval quality tracking
* Logging and observability
* Drift detection
* Evaluation pipelines
* Production-oriented AI workflows

---

## Roadmap

* Add MLflow-based evaluation tracking
* Add retrieval quality benchmark dataset
* Add hallucination and refusal tracking
* Add embedding drift simulation
* Add Prometheus metrics exporter
* Add Grafana dashboard
* Add automated re-indexing trigger
* Add Docker Compose deployment
* Add GitHub Actions CI/CD
* Add before/after drift simulation report

---

## Portfolio Highlight

> Developed a drift-aware LLMOps monitoring pipeline for RAG applications, enabling semantic retrieval, metadata-aware responses, request logging, retrieval quality monitoring, latency tracking, embedding drift detection, and automated re-indexing workflows using FastAPI, SentenceTransformers, ChromaDB, MLflow, Prometheus, and Grafana.

---

## License

This project is intended for educational and portfolio purposes.

---

## Author

**Trusha**

GitHub: [trush123ta](https://github.com/trush123ta)
