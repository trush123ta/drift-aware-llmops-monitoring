import re
from typing import Any, Dict, List


class RerankingService:
    def _tokens(self, text: str) -> set[str]:
        stopwords = {
            "what", "does", "how", "the", "and", "are", "for", "with",
            "that", "this", "from", "into", "using", "retrieval",
            "augmented", "generation", "rag", "measure", "role",
            "evaluation", "evaluated"
        }

        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

        return {
            token
            for token in tokens
            if token not in stopwords
        }

    def rerank(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        top_k: int,
    ) -> List[Dict[str, Any]]:
        query_tokens = self._tokens(query)

        reranked_contexts = []

        for context in retrieved_contexts:
            text = context.get("text", "")
            text_tokens = self._tokens(text)

            overlap = len(query_tokens.intersection(text_tokens))

            distance = float(context.get("distance", 1.0))

            semantic_score = 1.0 / (1.0 + distance)
            keyword_score = overlap / max(len(query_tokens), 1)

            final_score = (0.7 * semantic_score) + (0.3 * keyword_score)

            updated_context = context.copy()
            updated_context["rerank_score"] = final_score
            updated_context["keyword_overlap"] = overlap

            reranked_contexts.append(updated_context)

        reranked_contexts = sorted(
            reranked_contexts,
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return reranked_contexts[:top_k]


reranking_service = RerankingService()