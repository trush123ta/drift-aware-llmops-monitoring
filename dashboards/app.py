import json
from pathlib import Path

import pandas as pd
import streamlit as st


EVAL_REPORTS_DIR = Path("evaluation/reports")
DRIFT_REPORTS_DIR = Path("monitoring/reports")
LOG_FILE = Path("logs/rag_requests.jsonl")


st.set_page_config(
    page_title="Drift-Aware RAG Monitoring",
    layout="wide",
)


def get_latest_file(
    directory: Path,
    pattern: str,
    exclude_keywords: list[str] | None = None,
) -> Path | None:
    files = sorted(directory.glob(pattern))

    if exclude_keywords:
        files = [
            file
            for file in files
            if not any(keyword in file.name for keyword in exclude_keywords)
        ]

    if not files:
        return None

    return files[-1]


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_recent_logs(max_rows: int = 20) -> pd.DataFrame:
    if not LOG_FILE.exists():
        return pd.DataFrame()

    rows = []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    available_columns = [
        column
        for column in [
            "timestamp",
            "query",
            "retrieval_latency_ms",
            "generation_latency_ms",
            "total_latency_ms",
            "latency_ms",
        ]
        if column in df.columns
    ]

    return df[available_columns].tail(max_rows)


st.title("Drift-Aware LLMOps Monitoring Dashboard")
st.caption(
    "Monitoring dashboard for a local RAG pipeline with retrieval evaluation, "
    "answer evaluation, and drift detection."
)

retrieval_report_path = get_latest_file(
    EVAL_REPORTS_DIR,
    "retrieval_eval_*.json",
    exclude_keywords=["simulated"],
)

answer_report_path = get_latest_file(
    EVAL_REPORTS_DIR,
    "answer_eval_*.json",
)

drift_report_path = get_latest_file(
    DRIFT_REPORTS_DIR,
    "retrieval_drift_*.json",
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Retrieval Evaluation")

    if retrieval_report_path:
        retrieval_report = load_json(retrieval_report_path)

        st.metric("Hit Rate@k", f"{retrieval_report['hit_rate_at_k']:.2f}")
        st.metric("MRR@k", f"{retrieval_report['mrr_at_k']:.2f}")
        st.metric(
            "Avg Keyword Match",
            f"{retrieval_report.get('avg_keyword_match_score', 0):.2f}",
        )

        st.caption(f"Report: {retrieval_report_path.name}")
    else:
        st.warning("No retrieval evaluation report found.")

with col2:
    st.subheader("Answer Evaluation")

    if answer_report_path:
        answer_report = load_json(answer_report_path)

        st.metric(
            "Answer Keyword Match",
            f"{answer_report.get('avg_answer_keyword_match_score', 0):.2f}",
        )
        st.metric(
            "Citation Rate",
            f"{answer_report.get('citation_rate', 0):.2f}",
        )

        st.caption(f"Report: {answer_report_path.name}")
    else:
        st.warning("No answer evaluation report found.")

with col3:
    st.subheader("Retrieval Drift")

    if drift_report_path:
        drift_report = load_json(drift_report_path)

        drift_detected = drift_report.get("drift_detected", False)

        if drift_detected:
            st.error("Drift detected")
        else:
            st.success("No drift detected")

        st.metric(
            "Hit Rate Drop",
            f"{drift_report['metric_drops']['hit_rate_drop']:.2f}",
        )
        st.metric(
            "MRR Drop",
            f"{drift_report['metric_drops']['mrr_drop']:.2f}",
        )
        st.metric(
            "Keyword Match Drop",
            f"{drift_report['metric_drops']['keyword_match_drop']:.2f}",
        )

        st.caption(f"Report: {drift_report_path.name}")
    else:
        st.warning("No drift report found.")

st.divider()

st.subheader("Drift Recommendation")

if drift_report_path:
    drift_report = load_json(drift_report_path)
    st.info(drift_report.get("recommendation", "No recommendation available."))
else:
    st.warning("Run drift detection to generate a recommendation.")

st.divider()

st.subheader("Recent RAG API Latency")

logs_df = load_recent_logs()

if logs_df.empty:
    st.warning("No API logs found yet.")
else:
    st.dataframe(logs_df, use_container_width=True)

    latency_column = None

    if "total_latency_ms" in logs_df.columns:
        latency_column = "total_latency_ms"
    elif "latency_ms" in logs_df.columns:
        latency_column = "latency_ms"

    if latency_column:
        numeric_latency = pd.to_numeric(
            logs_df[latency_column],
            errors="coerce",
        ).dropna()

        if not numeric_latency.empty:
            st.line_chart(numeric_latency)