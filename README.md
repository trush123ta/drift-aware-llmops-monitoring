# Drift-Aware LLMOps Monitoring Pipeline

**A practical LLMOps project for monitoring Retrieval-Augmented Generation (RAG) systems using retrieval evaluation, answer evaluation, drift detection, and a local monitoring dashboard.**

This project focuses on a real post-deployment question:

> How do we know if a RAG system is still retrieving relevant context and generating grounded answers after documents, queries, or retrieval behavior change?

The current implementation builds a working local RAG monitoring pipeline with FastAPI, ChromaDB, SentenceTransformers, Ollama, JSONL logging, evaluation reports, retrieval drift detection, tests, Docker support, and a Streamlit dashboard.

---

## Project Motivation

Building a RAG application is only the first step. In real-world AI systems, retrieval and answer quality can silently degrade over time because of:

| Problem | Possible Signal |
|---|---|
| User query patterns change | Retrieval scores get worse |
| Document corpus changes | Hit Rate@k or MRR drops |
| Chunking/indexing quality changes | Relevant context appears lower in ranking |
| Retrieval behavior regresses | Keyword match and source relevance decrease |
| Answer grounding weakens | Citation rate or answer keyword match drops |
| System latency increases | Request latency trends upward |

This project monitors these signals and reports whether retrieval quality has drifted compared to a saved baseline.

---

## What This Project Does

The pipeline performs the following steps:

```text
PDF / Markdown documents
→ text cleaning
→ chunking with metadata
→ embedding generation
→ ChromaDB vector indexing
→ FastAPI RAG endpoint
→ semantic retrieval with reranking
→ context compression
→ Ollama local answer generation
→ citation-aware API response
→ JSONL request logging
→ retrieval evaluation
→ answer evaluation
→ retrieval drift detection
→ Streamlit monitoring dashboard
```

---

## Implemented Features

### 1. Knowledge Ingestion and Indexing

The ingestion pipeline supports local knowledge documents.

Implemented:

- PDF loading using PyMuPDF
- Markdown loading
- Text cleaning
- Noisy/reference chunk filtering
- Overlapping chunk generation
- Metadata extraction
- SentenceTransformer embeddings
- ChromaDB persistent vector store
- Ingestion report generation
- Indexed chunk preview generation

Main modules:

```text
indexing/
├── document_loader.py
├── chunker.py
├── embedder.py
├── vector_store.py
├── text_cleaner.py
└── ingest_docs.py
```

---

### 2. Online RAG Serving Layer

The FastAPI backend exposes a RAG API.

Implemented:

- `/health` endpoint
- `/query` endpoint
- Query embedding
- ChromaDB semantic retrieval
- Lightweight reranking
- Context compression
- Ollama-based local answer generation
- Source citation list
- Retrieval, generation, and total latency tracking

Main modules:

```text
app/
├── main.py
├── api/
│   └── routes.py
├── core/
│   └── config.py
├── schemas/
│   └── query.py
└── services/
    ├── retrieval_service.py
    ├── reranking_service.py
    ├── generation_service.py
    ├── context_service.py
    ├── source_service.py
    └── logging_service.py
```

---

### 3. Logging and Observability

Every API request is logged as structured JSONL.

Logged fields include:

- query
- generated answer
- retrieved contexts
- source metadata
- retrieval latency
- generation latency
- total latency
- compressed context used for generation

Logs are stored in:

```text
logs/rag_requests.jsonl
```

---

### 4. Retrieval Evaluation

The retrieval evaluator measures whether the retriever returns the expected source/page for evaluation questions.

Implemented metrics:

- Hit Rate@k
- MRR@k
- Average keyword match score

Current measured retrieval results:

| Metric | Score |
|---|---:|
| Hit Rate@5 | 0.40 |
| MRR@5 | 0.40 |
| Avg Keyword Match | 0.47 |

Evaluation files:

```text
evaluation/
├── datasets/
│   └── rag_eval_questions.json
├── retrieval_evaluator.py
├── answer_evaluator.py
└── view_latest_report.py
```

Reports are generated under:

```text
evaluation/reports/
```

Generated reports are ignored by Git by default.

---

### 5. Answer Evaluation

The answer evaluator checks generated answer quality using lightweight measurable signals.

Implemented metrics:

- Answer keyword match score
- Citation rate

Current measured answer results:

| Metric | Score |
|---|---:|
| Avg Answer Keyword Match | 0.37 |
| Citation Rate | 0.60 |

These scores are intentionally simple and transparent. They are useful for monitoring regressions over time, not for claiming perfect answer correctness.

---

### 6. Retrieval Drift Detection

Retrieval drift is calculated by comparing current retrieval metrics against a saved baseline.

Simple formula:

```text
Metric Drop = Baseline Metric - Current Metric
```

The detector monitors:

- Hit Rate@k drop
- MRR@k drop
- Avg keyword match drop

If one or more metric drops exceed the configured threshold, retrieval drift is flagged.

Example:

```text
Baseline Hit Rate@k = 0.40
Current Hit Rate@k  = 0.10
Hit Rate Drop       = 0.30

Drift detected = True
```

Drift detection modules:

```text
monitoring/
├── create_retrieval_baseline.py
├── retrieval_drift_detector.py
└── simulate_retrieval_drift.py
```

Current behavior:

```text
Normal evaluation report:      Drift detected = False
Simulated degraded report:     Drift detected = True
```

---

### 7. Streamlit Monitoring Dashboard

The current implemented dashboard is built with Streamlit.

It shows:

- Retrieval evaluation metrics
- Answer evaluation metrics
- Retrieval drift status
- Drift recommendation
- Recent RAG API latency logs
- Latency trend chart

Dashboard file:

```text
dashboards/app.py
```

Run with:

```bash
streamlit run dashboards/app.py
```

Note:

> The current working dashboard is Streamlit. Grafana and Prometheus are planned production extensions, not part of the current working implementation.

---

### 8. Tests

Basic tests are included for API health, drift metric calculation, and keyword matching.

Test folder:

```text
tests/
├── test_api.py
├── test_drift_detector.py
└── test_keyword_matching.py
```

Run tests:

```bash
pytest
```

Current result:

```text
3 passed
```

---

## Tech Stack

| Area | Current Tools |
|---|---|
| Language | Python 3.11 |
| Backend API | FastAPI, Uvicorn, Pydantic |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Local LLM | Ollama with llama3.2:3b |
| Document Parsing | PyMuPDF |
| Data Processing | Pandas, NumPy |
| Logging | JSONL |
| Evaluation Reports | JSON, CSV |
| Drift Detection | Custom Python metric comparison |
| Dashboard | Streamlit |
| Testing | Pytest |
| Containerization | Dockerfile, basic Docker Compose |

---

## Planned Production Extensions

These are intentionally listed as future extensions, not current implemented features:

| Extension | Purpose |
|---|---|
| Prometheus | Export runtime metrics for scraping |
| Grafana | Production-style monitoring dashboard |
| MLflow | Track evaluation experiments over time |
| GitHub Actions | Run tests automatically on push |
| Automated re-index trigger | Rebuild index automatically when drift is detected |
| Advanced embedding drift detection | Centroid shift, distribution shift, KL divergence, PSI |
| Stronger reranking | Cross-encoder reranker or LLM-based reranking |

---

## Repository Structure

```text
drift-aware-llmops-monitoring/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── query.py
│   └── services/
│       ├── retrieval_service.py
│       ├── reranking_service.py
│       ├── generation_service.py
│       ├── context_service.py
│       ├── source_service.py
│       └── logging_service.py
│
├── indexing/
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── text_cleaner.py
│   └── ingest_docs.py
│
├── evaluation/
│   ├── datasets/
│   │   └── rag_eval_questions.json
│   ├── retrieval_evaluator.py
│   ├── answer_evaluator.py
│   └── view_latest_report.py
│
├── monitoring/
│   ├── baselines/
│   ├── create_retrieval_baseline.py
│   ├── retrieval_drift_detector.py
│   └── simulate_retrieval_drift.py
│
├── dashboards/
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   ├── test_drift_detector.py
│   └── test_keyword_matching.py
│
├── data/
│   ├── raw_docs/
│   ├── raw_pdfs/
│   ├── processed/
│   └── vector_db/
│
├── logs/
│   └── rag_requests.jsonl
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/trush123ta/drift-aware-llmops-monitoring.git
cd drift-aware-llmops-monitoring
```

### 2. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from the official website, then pull the model:

```bash
ollama pull llama3.2:3b
```

Start Ollama:

```bash
ollama serve
```

If Ollama is already running in the background, this command may not be needed.

---

## Running the Project

### 1. Add source documents

Place Markdown files in:

```text
data/raw_docs/
```

Place PDF files in:

```text
data/raw_pdfs/
```

### 2. Build the vector index

```bash
python -m indexing.ingest_docs
```

This creates or updates the local ChromaDB index in:

```text
data/vector_db/
```

### 3. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

### 4. Query the RAG API

Endpoint:

```http
POST /query
```

Example request:

```json
{
  "query": "How is retrieval augmented generation evaluated?",
  "top_k": 3
}
```

Example response shape:

```json
{
  "query": "How is retrieval augmented generation evaluated?",
  "answer": "The answer is generated using retrieved context and includes citations such as [S1].",
  "sources": [
    {
      "source_id": "S1",
      "source": "rag_evaluation_survey.pdf",
      "source_type": "pdf",
      "page": 5,
      "chunk_id": "rag_evaluation_survey.pdf_p5_c0",
      "distance": 0.73
    }
  ],
  "retrieved_contexts": [],
  "retrieval_latency_ms": 92.1,
  "generation_latency_ms": 19846.4,
  "total_latency_ms": 19938.5,
  "note": "Lower distance means higher semantic similarity. Answer generation uses compressed retrieved context."
}
```

---

## Evaluation and Drift Commands

### Run retrieval evaluation

```bash
python -m evaluation.retrieval_evaluator
```

### View latest retrieval report

```bash
python -m evaluation.view_latest_report
```

### Run answer evaluation

```bash
python -m evaluation.answer_evaluator
```

### Create retrieval baseline

```bash
python -m monitoring.create_retrieval_baseline
```

### Run retrieval drift detection

```bash
python -m monitoring.retrieval_drift_detector
```

### Simulate degraded retrieval

```bash
python -m monitoring.simulate_retrieval_drift
python -m monitoring.retrieval_drift_detector
```

---

## Run the Dashboard

```bash
streamlit run dashboards/app.py
```

The dashboard reads from generated evaluation reports, drift reports, and JSONL logs.

---

## Run Tests

```bash
pytest
```

Expected current result:

```text
3 passed
```

---

## Docker Usage

The Dockerfile containerizes the FastAPI application.

Build image:

```bash
docker build -t drift-aware-rag .
```

Run container:

```bash
docker run -p 8000:8000 drift-aware-rag
```

Important:

> Ollama should be running separately on the host machine unless Docker Compose is extended to include an Ollama service.

### Docker Compose

The current `docker-compose.yml` can be used for a basic local container run, depending on your local configuration.

```bash
docker compose up
```

In this project, Docker Compose is mainly a foundation for future production-style extensions such as Prometheus, Grafana, MLflow, or a separate Ollama service.

---

## Current Results

### Retrieval Quality

| Metric | Current Score |
|---|---:|
| Hit Rate@5 | 0.40 |
| MRR@5 | 0.40 |
| Avg Keyword Match | 0.47 |

### Answer Quality

| Metric | Current Score |
|---|---:|
| Avg Answer Keyword Match | 0.37 |
| Citation Rate | 0.60 |

### Drift Detection

| Scenario | Result |
|---|---|
| Current report similar to baseline | Drift detected = False |
| Simulated degraded report | Drift detected = True |

---

## Interview Explanation

A short way to explain the project:

> I built a drift-aware LLMOps monitoring pipeline for RAG systems. It ingests PDFs and Markdown documents, chunks and indexes them in ChromaDB, retrieves context with reranking, generates grounded answers using a local Ollama model, logs each request, evaluates retrieval and answer quality, detects retrieval drift against a saved baseline, and visualizes system health in a Streamlit dashboard.

For retrieval drift:

> Retrieval drift is calculated as degradation from a saved baseline. I compare current Hit Rate@k, MRR@k, and keyword-match score against baseline values. If the drop exceeds a threshold, the system flags drift and recommends reviewing the index, chunking, embeddings, or reranking strategy.

For Grafana:

> The current implementation uses Streamlit for lightweight local monitoring. Grafana and Prometheus are planned production extensions for a more infrastructure-oriented deployment.

---

## Why This Project Is Valuable

This project demonstrates more than building a chatbot. It shows a production-minded RAG lifecycle:

- Document ingestion and indexing
- Vector search
- Local LLM-based answer generation
- Grounded response design with citations
- Request logging
- Quantitative retrieval evaluation
- Quantitative answer evaluation
- Drift detection against a baseline
- Monitoring dashboard
- Testing and containerization basics
- Clear distinction between implemented features and planned production extensions

---

## Limitations

Current limitations:

- Evaluation dataset is small
- Answer evaluation uses lightweight keyword and citation metrics
- No full LLM-as-judge evaluation yet
- No Prometheus/Grafana integration yet
- No MLflow experiment tracking yet
- No automatic re-indexing trigger yet
- Ollama must run locally for answer generation
- Local LLM latency depends on machine performance

---

## Future Work

Planned next improvements:

- Add Prometheus metrics endpoint
- Add Grafana dashboard
- Add MLflow experiment tracking
- Add GitHub Actions CI workflow
- Add automated re-index trigger
- Expand evaluation dataset
- Add stronger reranking
- Add more robust answer faithfulness scoring
- Add dashboard screenshots to README

---

## License

This project is intended for educational and portfolio purposes.

---

## Author

**Trusha**

GitHub: [trush123ta](https://github.com/trush123ta)
