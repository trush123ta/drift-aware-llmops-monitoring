from typing import List, Dict


def generate_answer(query: str, retrieved_contexts: List[Dict]) -> str:
    if not retrieved_contexts:
        return "I could not find relevant context to answer this query."

    best_context = retrieved_contexts[0]["text"]

    answer = (
        "Based on the retrieved knowledge base, "
        f"{best_context}"
    )

    return answer