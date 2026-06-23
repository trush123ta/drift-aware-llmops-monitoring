import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from app.services.context_service import context_service
from app.services.generation_service import generation_service
from app.services.retrieval_service import retrieval_service
from app.services.source_service import source_service


DATASET_PATH = Path("evaluation/datasets/rag_eval_questions.json")
REPORTS_DIR = Path("evaluation/reports")


def load_eval_dataset() -> List[Dict[str, Any]]:
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def answer_keyword_match_score(
    answer: str,
    expected_keywords: List[str],
) -> float:
    if not expected_keywords:
        return 0.0

    answer_lower = answer.lower()
    matched_scores = []

    for keyword in expected_keywords:
        keyword_lower = keyword.lower().strip()

        if keyword_lower in answer_lower:
            matched_scores.append(1.0)
            continue

        keyword_tokens = [
            token
            for token in keyword_lower.split()
            if len(token) > 2
        ]

        if not keyword_tokens:
            matched_scores.append(0.0)
            continue

        matched_tokens = [
            token
            for token in keyword_tokens
            if token in answer_lower
        ]

        matched_scores.append(len(matched_tokens) / len(keyword_tokens))

    return sum(matched_scores) / len(expected_keywords)


def citation_present(answer: str) -> bool:
    return "[S" in answer and "]" in answer


def evaluate_answers(top_k: int = 5, generation_top_n: int = 1) -> Dict[str, Any]:
    dataset = load_eval_dataset()
    results = []

    keyword_scores = []
    citation_count = 0

    for item in dataset:
        question = item["question"]
        expected_keywords = item.get("expected_keywords", [])

        retrieved_contexts = retrieval_service.retrieve(
            query=question,
            top_k=top_k,
        )

        contexts_for_generation = retrieved_contexts[:generation_top_n]

        compressed_contexts = context_service.compress_contexts(
            query=question,
            retrieved_contexts=contexts_for_generation,
        )

        answer = generation_service.generate_answer(
            query=question,
            retrieved_contexts=compressed_contexts,
        )

        sources = source_service.build_sources(retrieved_contexts)

        keyword_score = answer_keyword_match_score(
            answer=answer,
            expected_keywords=expected_keywords,
        )

        has_citation = citation_present(answer)

        if has_citation:
            citation_count += 1

        keyword_scores.append(keyword_score)

        results.append(
            {
                "question": question,
                "answer": answer,
                "expected_keywords": expected_keywords,
                "answer_keyword_match_score": keyword_score,
                "citation_present": has_citation,
                "top_source": sources[0] if sources else None,
                "sources": sources,
            }
        )

    total_questions = len(dataset)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "top_k": top_k,
        "generation_top_n": generation_top_n,
        "total_questions": total_questions,
        "avg_answer_keyword_match_score": (
            sum(keyword_scores) / total_questions if total_questions else 0
        ),
        "citation_rate": (
            citation_count / total_questions if total_questions else 0
        ),
        "results": results,
    }

    return report


def save_json_report(report: Dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"answer_eval_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return report_path


def save_csv_summary(report: Dict[str, Any], json_report_path: Path) -> Path:
    csv_path = json_report_path.with_suffix(".csv")

    rows = []

    for result in report["results"]:
        top_source = result.get("top_source") or {}

        rows.append(
            {
                "question": result["question"],
                "answer_keyword_match_score": result["answer_keyword_match_score"],
                "citation_present": result["citation_present"],
                "top_1_source": top_source.get("source"),
                "top_1_page": top_source.get("page"),
                "top_1_chunk_id": top_source.get("chunk_id"),
                "answer": result["answer"],
            }
        )

    fieldnames = [
        "question",
        "answer_keyword_match_score",
        "citation_present",
        "top_1_source",
        "top_1_page",
        "top_1_chunk_id",
        "answer",
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return csv_path


if __name__ == "__main__":
    evaluation_report = evaluate_answers(top_k=5, generation_top_n=1)
    json_path = save_json_report(evaluation_report)
    csv_path = save_csv_summary(evaluation_report, json_path)

    print("Answer evaluation completed.")
    print(f"Top-k: {evaluation_report['top_k']}")
    print(f"Generation top-n: {evaluation_report['generation_top_n']}")
    print(f"Total questions: {evaluation_report['total_questions']}")
    print(
        "Avg Answer Keyword Match: "
        f"{evaluation_report['avg_answer_keyword_match_score']:.2f}"
    )
    print(f"Citation Rate: {evaluation_report['citation_rate']:.2f}")
    print(f"Saved JSON report to: {json_path}")
    print(f"Saved CSV summary to: {csv_path}")