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

## Current Project Status

### Implemented

* FastAPI-based RAG API
* Semantic retrieval using SentenceTransformers
* ChromaDB vector database
* Local document ingestion pipeline
* Request logging in JSONL format
* Retrieval distance tracking
* Latency tracking
* Basic RAG log analysis script
* GitHub-based version control

### Planned

* MLflow experiment tracking
* Retrieval quality evaluation dataset
* Embedding drift detection
* Accuracy drop detection
* Hallucination/refusal tracking
* Prometheus metrics endpoint
* Grafana dashboard
* Automated re-indexing trigger
* Before/after evaluation report
* Docker setup
* GitHub Actions CI/CD

---

## Architecture

```text
User Query
    ↓
FastAPI /query Endpoint
    ↓
SentenceTransformer Embedding Model
    ↓
ChromaDB Vector Search
    ↓
Top-k Document Retrieval
    ↓
Response Returned to User
    ↓
Request Logging
    ↓
Monitoring & Analysis
    ↓
Drift / Quality Detection
    ↓
Re-indexing or Evaluation Trigger
```

---

## Repository Structure

```text
drift-aware-llmops-monitoring/
│
├── app/
│   ├── main.py                 # FastAPI application
│   ├── rag_pipeline.py          # Semantic retrieval pipeline
│   └── logger.py                # JSONL request logging
│
├── indexing/
│   └── ingest_docs.py           # Builds ChromaDB vector index
│
├── monitoring/
│   └── analyze_logs.py          # Basic monitoring summary from logs
│
├── evaluation/
│   └── .gitkeep                 # Future evaluation scripts
│
├── dashboards/
│   └── .gitkeep                 # Future Grafana dashboard files
│
├── data/
│   └── knowledge_base.txt       # Sample knowledge base
│
├── logs/
│   └── rag_requests.jsonl       # Runtime logs, ignored by Git
│
├── tests/
│   └── .gitkeep                 # Future tests
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Tech Stack

| Component           | Tool                   |
| ------------------- | ---------------------- |
| API                 | FastAPI                |
| Server              | Uvicorn                |
| Embeddings          | SentenceTransformers   |
| Embedding Model     | all-MiniLM-L6-v2       |
| Vector Database     | ChromaDB               |
| Logging             | JSONL                  |
| Monitoring          | Custom Python scripts  |
| Experiment Tracking | MLflow planned         |
| Metrics             | Prometheus planned     |
| Dashboard           | Grafana planned        |
| Containerization    | Docker planned         |
| CI/CD               | GitHub Actions planned |

---

## Embedding Model

This project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This is a lightweight embedding model that converts text into numerical vectors.

Example:

```text
"How can I monitor model performance?"
        ↓
[0.12, -0.34, 0.87, ...]
```

These embeddings are stored in ChromaDB and used for semantic retrieval.

The model is used because it is:

* Lightweight
* Fast
* Free to run locally
* Suitable for semantic search
* Good for RAG prototypes
* Independent of paid API services

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/trush123ta/drift-aware-llmops-monitoring.git
cd drift-aware-llmops-monitoring
```

---

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If activation is blocked, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Build the Vector Index

```bash
python indexing/ingest_docs.py
```

Expected output:

```text
Indexed 6 documents.
```

This creates a local ChromaDB vector database inside:

```text
data/vector_db/
```

---

### 5. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## API Usage

### Health Check

```http
GET /
```

Example response:

```json
{
  "status": "ok",
  "message": "LLMOps monitoring pipeline is running"
}
```

---

### Query Endpoint

```http
POST /query
```

Example request:

```json
{
  "query": "How can I monitor model performance?",
  "top_k": 3
}
```

Example response:

```json
{
  "query": "How can I monitor model performance?",
  "retrieved_docs": [
    "MLflow is used for experiment tracking and model lifecycle management.",
    "Prometheus is commonly used for monitoring machine learning systems.",
    "Grafana is used to visualize metrics and dashboards."
  ],
  "retrieval_distances": [
    1.2584,
    1.3454,
    1.5065
  ],
  "latency_ms": 97.08,
  "note": "Lower distance means higher semantic similarity."
}
```

---

## Logging

Every API request is logged to:

```text
logs/rag_requests.jsonl
```

Example log entry:

```json
{
  "query": "How can I monitor model performance?",
  "retrieved_docs": [
    "MLflow is used for experiment tracking and model lifecycle management.",
    "Prometheus is commonly used for monitoring machine learning systems.",
    "Grafana is used to visualize metrics and dashboards."
  ],
  "retrieval_distances": [
    1.2584,
    1.3454,
    1.5065
  ],
  "latency_ms": 97.08,
  "note": "Lower distance means higher semantic similarity.",
  "timestamp": "2026-06-10T18:21:58Z"
}
```

Runtime logs are ignored by Git to avoid committing generated files.

---

## Monitoring

The current monitoring script reads request logs and calculates:

* Total number of queries
* Average latency
* Average retrieval distance
* Worst retrieval query

Run:

```bash
python monitoring/analyze_logs.py
```

Example output:

```text
RAG Monitoring Summary
----------------------
Total queries: 5
Average latency: 102.45 ms
Average retrieval distance: 1.3842
Worst retrieval query: How do I detect hallucinations?
```

---

## Why Retrieval Distance Matters

The vector database returns a distance score for each retrieved document.

```text
Lower retrieval distance = higher semantic similarity
Higher retrieval distance = weaker match
```

Tracking this over time helps detect retrieval degradation.

For example:

```text
Baseline average retrieval distance: 1.20
Current average retrieval distance: 1.80
```

This could indicate that user queries are drifting away from the indexed knowledge base or that the current index is no longer sufficient.

---

## Planned Drift Detection Logic

The planned drift detection module will compare baseline and current query embeddings.

Example logic:

```text
Baseline query embeddings
        ↓
Current query embeddings
        ↓
Distribution comparison
        ↓
Drift score
        ↓
Alert or re-indexing trigger
```

Possible drift indicators:

* Increase in average retrieval distance
* Drop in retrieval precision
* Change in query embedding distribution
* Increase in unanswered queries
* Increase in hallucination/refusal rate

---

## Planned Evaluation Module

The evaluation module will use a small benchmark dataset containing:

```json
{
  "question": "What is embedding drift?",
  "expected_answer": "Embedding drift occurs when embedding distributions change over time.",
  "expected_sources": ["embedding_drift_doc"]
}
```

Planned metrics:

* Retrieval precision
* Retrieval recall
* Answer correctness
* Faithfulness
* Hallucination rate
* Refusal rate
* Latency
* Before/after re-indexing performance

---

## Planned MLflow Tracking

MLflow will be used to track evaluation runs.

Planned logged metrics:

```text
retrieval_precision
retrieval_recall
average_retrieval_distance
latency_ms
hallucination_rate
refusal_rate
drift_score
reindexing_status
```

This will make it possible to compare system performance before and after re-indexing.

---

## Planned Prometheus and Grafana Monitoring

Prometheus will expose live metrics such as:

```text
rag_request_count
rag_average_latency_ms
rag_average_retrieval_distance
rag_hallucination_rate
rag_refusal_rate
rag_drift_score
```

Grafana will visualize:

* Request volume
* Latency trends
* Retrieval quality trends
* Drift score trends
* Hallucination/refusal spikes
* Re-indexing events

---

## Planned Automated Re-indexing Trigger

The re-indexing trigger will activate when retrieval quality drops below a threshold.

Example rule:

```python
if current_avg_retrieval_distance > baseline_avg_retrieval_distance + threshold:
    trigger_reindexing()
```

The pipeline will then:

```text
Detect degradation
    ↓
Trigger re-indexing
    ↓
Rebuild vector database
    ↓
Run evaluation
    ↓
Compare before/after metrics
    ↓
Log results to MLflow
```

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
* Drift detection concepts
* Evaluation pipelines
* Production-oriented AI workflows

---

## Resume/CV Line

Developed a drift-aware LLMOps monitoring pipeline for RAG applications, enabling semantic retrieval, request logging, retrieval quality monitoring, latency tracking, embedding drift detection design, and automated re-indexing workflows using FastAPI, SentenceTransformers, ChromaDB, MLflow, Prometheus, and Grafana.

---

## Future Improvements

* Replace sample knowledge base with real documents
* Add document chunking
* Add metadata-aware retrieval
* Add hybrid search
* Add LLM-based answer generation
* Add RAG faithfulness evaluation
* Add CI/CD tests
* Add Docker Compose deployment
* Add Grafana dashboard screenshots
* Add before/after drift simulation report

---

## License

This project is intended for educational and portfolio purposes.

---

## Author

**Trusha**

GitHub: [trush123ta](https://github.com/trush123ta)
