import json
import shutil
from pathlib import Path


EVAL_REPORTS_DIR = Path("evaluation/reports")
BASELINE_DIR = Path("monitoring/baselines")
BASELINE_PATH = BASELINE_DIR / "retrieval_baseline.json"


def get_latest_retrieval_report() -> Path:
    reports = sorted(EVAL_REPORTS_DIR.glob("retrieval_eval_*.json"))

    if not reports:
        raise FileNotFoundError(
            "No retrieval evaluation reports found. "
            "Run python -m evaluation.retrieval_evaluator first."
        )

    return reports[-1]


def create_baseline() -> None:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)

    latest_report = get_latest_retrieval_report()

    with open(latest_report, "r", encoding="utf-8") as file:
        report = json.load(file)

    baseline = {
        "source_report": str(latest_report),
        "timestamp": report["timestamp"],
        "top_k": report["top_k"],
        "total_questions": report["total_questions"],
        "hit_rate_at_k": report["hit_rate_at_k"],
        "mrr_at_k": report["mrr_at_k"],
        "avg_keyword_match_score": report["avg_keyword_match_score"],
    }

    with open(BASELINE_PATH, "w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=2)

    archived_report_path = BASELINE_DIR / latest_report.name
    shutil.copy(latest_report, archived_report_path)

    print("Retrieval baseline created.")
    print(f"Baseline source report: {latest_report}")
    print(f"Saved baseline to: {BASELINE_PATH}")
    print(f"Archived full report to: {archived_report_path}")
    print()
    print("Baseline metrics:")
    print(f"Hit Rate@k: {baseline['hit_rate_at_k']:.2f}")
    print(f"MRR@k: {baseline['mrr_at_k']:.2f}")
    print(f"Avg Keyword Match: {baseline['avg_keyword_match_score']:.2f}")


if __name__ == "__main__":
    create_baseline()