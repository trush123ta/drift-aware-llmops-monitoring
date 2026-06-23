import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from app.services.retrieval_service import retrieval_service


DATASET_PATH = Path("evaluation/datasets/rag_eval_questions.json")
REPORTS_DIR = Path("evaluation/reports")


def load_eval_dataset() -> List[Dict[str, Any]]:
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def is_expected_context_found(
    retrieved_contexts: List[Dict[str, Any]],
    expected_source: str,
    expected_page: int,
) -> bool:
    for context in retrieved_contexts:
        if (
            context.get("source") == expected_source
            and context.get("page") == expected_page
        ):
            return True

    return False


def reciprocal_rank(
    retrieved_contexts: List[Dict[str, Any]],
    expected_source: str,
    expected_page: int,
) -> float:
    for index, context in enumerate(retrieved_contexts, start=1):
        if (
            context.get("source") == expected_source
            and context.get("page") == expected_page
        ):
            return 1.0 / index

    return 0.0


def keyword_match_score(
    retrieved_contexts: List[Dict[str, Any]],
    expected_keywords: List[str],
) -> float:
    """
    Measures whether retrieved contexts contain the expected concepts.

    Supports both exact phrase matches and partial token-level matches.
    This avoids overly harsh scoring when the retrieved text uses a slightly
    different wording than the expected keyword phrase.
    """
    if not expected_keywords:
        return 0.0

    combined_text = " ".join(
        context.get("text", "").lower()
        for context in retrieved_contexts
    )

    matched_scores = []

    for keyword in expected_keywords:
        keyword_lower = keyword.lower().strip()

        # Full phrase match
        if keyword_lower in combined_text:
            matched_scores.append(1.0)
            continue

        # Partial token match for multi-word concepts
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
            if token in combined_text
        ]

        matched_scores.append(len(matched_tokens) / len(keyword_tokens))

    return sum(matched_scores) / len(expected_keywords)


def evaluate_retrieval(top_k: int = 5) -> Dict[str, Any]:
    dataset = load_eval_dataset()
    results = []

    hit_count = 0
    reciprocal_ranks = []

    for item in dataset:
        question = item["question"]
        expected_source = item["expected_source"]
        expected_page = item["expected_page"]
        expected_keywords = item.get("expected_keywords", [])

        retrieved_contexts = retrieval_service.retrieve(
            query=question,
            top_k=top_k,
        )

        hit = is_expected_context_found(
            retrieved_contexts=retrieved_contexts,
            expected_source=expected_source,
            expected_page=expected_page,
        )

        rr = reciprocal_rank(
            retrieved_contexts=retrieved_contexts,
            expected_source=expected_source,
            expected_page=expected_page,
        )

        keyword_score = keyword_match_score(
            retrieved_contexts=retrieved_contexts,
            expected_keywords=expected_keywords,
        )

        if hit:
            hit_count += 1

        reciprocal_ranks.append(rr)

        results.append(
            {
                "question": question,
                "expected_source": expected_source,
                "expected_page": expected_page,
                "expected_keywords": expected_keywords,
                "hit_at_k": hit,
                "reciprocal_rank": rr,
                "keyword_match_score": keyword_score,
                "top_retrieved": [
                    {
                        "rank": rank,
                        "source": context.get("source"),
                        "page": context.get("page"),
                        "chunk_id": context.get("chunk_id"),
                        "distance": context.get("distance"),
                    }
                    for rank, context in enumerate(retrieved_contexts, start=1)
                ],
            }
        )

    total_questions = len(dataset)

    keyword_scores = [
        result["keyword_match_score"]
        for result in results
    ]

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "top_k": top_k,
        "total_questions": total_questions,
        "hit_rate_at_k": hit_count / total_questions if total_questions else 0,
        "mrr_at_k": (
            sum(reciprocal_ranks) / total_questions if total_questions else 0
        ),
        "avg_keyword_match_score": (
            sum(keyword_scores) / total_questions if total_questions else 0
        ),
        "results": results,
    }

    return report


def save_report(report: Dict[str, Any]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"retrieval_eval_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return report_path


if __name__ == "__main__":
    evaluation_report = evaluate_retrieval(top_k=5)
    saved_path = save_report(evaluation_report)

    print("Retrieval evaluation completed.")
    print(f"Top-k: {evaluation_report['top_k']}")
    print(f"Total questions: {evaluation_report['total_questions']}")
    print(f"Hit Rate@k: {evaluation_report['hit_rate_at_k']:.2f}")
    print(f"MRR@k: {evaluation_report['mrr_at_k']:.2f}")
    print(
        "Avg Keyword Match: "
        f"{evaluation_report['avg_keyword_match_score']:.2f}"
    )
    print(f"Saved report to: {saved_path}")