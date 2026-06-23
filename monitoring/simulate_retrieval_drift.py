import json
from datetime import datetime, timezone
from pathlib import Path


EVAL_REPORTS_DIR = Path("evaluation/reports")
SIMULATED_REPORT_PATH = EVAL_REPORTS_DIR / "retrieval_eval_simulated_drift.json"


def get_latest_retrieval_report() -> Path:
    reports = sorted(EVAL_REPORTS_DIR.glob("retrieval_eval_*.json"))

    if not reports:
        raise FileNotFoundError(
            "No retrieval evaluation reports found. "
            "Run python -m evaluation.retrieval_evaluator first."
        )

    return reports[-1]


def simulate_drift() -> None:
    latest_report_path = get_latest_retrieval_report()

    with open(latest_report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    degraded_report = report.copy()
    degraded_report["timestamp"] = datetime.now(timezone.utc).isoformat()
    degraded_report["hit_rate_at_k"] = max(0.0, report["hit_rate_at_k"] - 0.30)
    degraded_report["mrr_at_k"] = max(0.0, report["mrr_at_k"] - 0.30)
    degraded_report["avg_keyword_match_score"] = max(
        0.0,
        report["avg_keyword_match_score"] - 0.30,
    )

    with open(SIMULATED_REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(degraded_report, file, indent=2)

    print("Simulated retrieval drift report created.")
    print(f"Source report: {latest_report_path}")
    print(f"Saved simulated report to: {SIMULATED_REPORT_PATH}")
    print()
    print("Original metrics:")
    print(f"  Hit Rate@k: {report['hit_rate_at_k']:.2f}")
    print(f"  MRR@k: {report['mrr_at_k']:.2f}")
    print(f"  Avg Keyword Match: {report['avg_keyword_match_score']:.2f}")
    print()
    print("Degraded metrics:")
    print(f"  Hit Rate@k: {degraded_report['hit_rate_at_k']:.2f}")
    print(f"  MRR@k: {degraded_report['mrr_at_k']:.2f}")
    print(
        "  Avg Keyword Match: "
        f"{degraded_report['avg_keyword_match_score']:.2f}"
    )


if __name__ == "__main__":
    simulate_drift()