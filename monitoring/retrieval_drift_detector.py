import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


EVAL_REPORTS_DIR = Path("evaluation/reports")
BASELINE_PATH = Path("monitoring/baselines/retrieval_baseline.json")
DRIFT_REPORTS_DIR = Path("monitoring/reports")


THRESHOLDS = {
    "hit_rate_drop": 0.20,
    "mrr_drop": 0.20,
    "keyword_match_drop": 0.20,
}


def load_baseline() -> Dict[str, Any]:
    if not BASELINE_PATH.exists():
        raise FileNotFoundError(
            "No retrieval baseline found. "
            "Run python -m monitoring.create_retrieval_baseline first."
        )

    with open(BASELINE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_latest_retrieval_report() -> Path:
    reports = sorted(
        report
        for report in EVAL_REPORTS_DIR.glob("retrieval_eval_*.json")
        if "simulated" not in report.name
    )

    if not reports:
        raise FileNotFoundError(
            "No non-simulated retrieval evaluation reports found. "
            "Run python -m evaluation.retrieval_evaluator first."
        )

    return reports[-1]


def load_current_report() -> Dict[str, Any]:
    latest_report = get_latest_retrieval_report()

    with open(latest_report, "r", encoding="utf-8") as file:
        report = json.load(file)

    report["report_path"] = str(latest_report)

    return report


def metric_drop(baseline_value: float, current_value: float) -> float:
    return round(baseline_value - current_value, 4)


def detect_retrieval_drift() -> Dict[str, Any]:
    baseline = load_baseline()
    current = load_current_report()

    hit_rate_drop = metric_drop(
        baseline["hit_rate_at_k"],
        current["hit_rate_at_k"],
    )
    mrr_drop = metric_drop(
        baseline["mrr_at_k"],
        current["mrr_at_k"],
    )
    keyword_match_drop = metric_drop(
        baseline["avg_keyword_match_score"],
        current["avg_keyword_match_score"],
    )

    drift_signals = {
        "hit_rate_drift": hit_rate_drop >= THRESHOLDS["hit_rate_drop"],
        "mrr_drift": mrr_drop >= THRESHOLDS["mrr_drop"],
        "keyword_match_drift": (
            keyword_match_drop >= THRESHOLDS["keyword_match_drop"]
        ),
    }

    drift_detected = any(drift_signals.values())

    recommendation = (
        "Retrieval quality degradation detected. Review recent document changes, "
        "embedding/index updates, chunking configuration, and reranking settings. "
        "Consider rebuilding the index or updating retrieval strategy."
        if drift_detected
        else "No significant retrieval drift detected."
    )

    drift_report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "baseline_source_report": baseline["source_report"],
        "current_source_report": current["report_path"],
        "thresholds": THRESHOLDS,
        "baseline_metrics": {
            "hit_rate_at_k": baseline["hit_rate_at_k"],
            "mrr_at_k": baseline["mrr_at_k"],
            "avg_keyword_match_score": baseline["avg_keyword_match_score"],
        },
        "current_metrics": {
            "hit_rate_at_k": current["hit_rate_at_k"],
            "mrr_at_k": current["mrr_at_k"],
            "avg_keyword_match_score": current["avg_keyword_match_score"],
        },
        "metric_drops": {
            "hit_rate_drop": hit_rate_drop,
            "mrr_drop": mrr_drop,
            "keyword_match_drop": keyword_match_drop,
        },
        "drift_signals": drift_signals,
        "drift_detected": drift_detected,
        "recommendation": recommendation,
    }

    return drift_report


def save_drift_report(report: Dict[str, Any]) -> Path:
    DRIFT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = DRIFT_REPORTS_DIR / f"retrieval_drift_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return report_path


if __name__ == "__main__":
    report = detect_retrieval_drift()
    saved_path = save_drift_report(report)

    print("Retrieval drift detection completed.")
    print(f"Baseline report: {report['baseline_source_report']}")
    print(f"Current report: {report['current_source_report']}")
    print()
    print("Baseline metrics:")
    print(f"  Hit Rate@k: {report['baseline_metrics']['hit_rate_at_k']:.2f}")
    print(f"  MRR@k: {report['baseline_metrics']['mrr_at_k']:.2f}")
    print(
        "  Avg Keyword Match: "
        f"{report['baseline_metrics']['avg_keyword_match_score']:.2f}"
    )
    print()
    print("Current metrics:")
    print(f"  Hit Rate@k: {report['current_metrics']['hit_rate_at_k']:.2f}")
    print(f"  MRR@k: {report['current_metrics']['mrr_at_k']:.2f}")
    print(
        "  Avg Keyword Match: "
        f"{report['current_metrics']['avg_keyword_match_score']:.2f}"
    )
    print()
    print("Metric drops:")
    print(f"  Hit Rate Drop: {report['metric_drops']['hit_rate_drop']:.2f}")
    print(f"  MRR Drop: {report['metric_drops']['mrr_drop']:.2f}")
    print(
        "  Keyword Match Drop: "
        f"{report['metric_drops']['keyword_match_drop']:.2f}"
    )
    print()
    print(f"Drift detected: {report['drift_detected']}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Saved drift report to: {saved_path}")