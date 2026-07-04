from evaluation.retrieval_evaluator import keyword_match_score


def test_keyword_match_score_exact_match():
    retrieved_contexts = [
        {
            "text": "RAG evaluation includes relevance, accuracy, faithfulness, and correctness."
        }
    ]

    expected_keywords = [
        "relevance",
        "accuracy",
        "faithfulness",
        "correctness",
    ]

    score = keyword_match_score(retrieved_contexts, expected_keywords)

    assert score == 1.0