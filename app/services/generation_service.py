from typing import List, Dict, Any


class GenerationService:
    def generate_answer(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
    ) -> str:
        if not retrieved_contexts:
            return "I could not find relevant context to answer this query."

        best_context = retrieved_contexts[0]["text"]

        return f"Based on the retrieved knowledge base, {best_context}"


generation_service = GenerationService()