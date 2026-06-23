import json
from pathlib import Path


REPORTS_DIR = Path("evaluation/reports")


def get_latest_report() -> Path:
    reports = sorted(REPORTS_DIR.glob("retrieval_eval_*.json"))

    if not reports:
        raise FileNotFoundError("No retrieval evaluation reports found.")

    return reports[-1]


def main() -> None:
    report_path = get_latest_report()

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    print(f"Report: {report_path}")
    print(f"Top-k: {report['top_k']}")
    print(f"Total questions: {report['total_questions']}")
    print(f"Hit Rate@k: {report['hit_rate_at_k']:.2f}")
    print(f"MRR@k: {report['mrr_at_k']:.2f}")
    print(f"Avg Keyword Match: {report.get('avg_keyword_match_score', 0):.2f}")
    print()

    for index, result in enumerate(report["results"], start=1):
        status = "PASS" if result["hit_at_k"] else "FAIL"

        print("=" * 80)
        print(f"{index}. {status}")
        print(f"Question: {result['question']}")
        print(
            f"Expected: {result['expected_source']} "
            f"page {result['expected_page']}"
        )
        print(f"Keyword Match: {result.get('keyword_match_score', 0):.2f}")

        expected_keywords = result.get("expected_keywords", [])
        if expected_keywords:
            print(f"Expected keywords: {', '.join(expected_keywords)}")

        print("Top retrieved:")

        for retrieved in result["top_retrieved"]:
            print(
                f"  Rank {retrieved['rank']}: "
                f"{retrieved['source']} page {retrieved['page']} "
                f"distance={retrieved['distance']:.4f}"
            )


if __name__ == "__main__":
    main()