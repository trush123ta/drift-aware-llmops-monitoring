from typing import Any, Dict, List


class ContextService:
    def compress_contexts(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        max_sentences_per_context: int = 4,
    ) -> List[Dict[str, Any]]:
        query_terms = set(query.lower().split())
        compressed_contexts = []

        for context in retrieved_contexts:
            text = context.get("text", "")
            sentences = text.replace("\n", " ").split(". ")

            scored_sentences = []

            for sentence in sentences:
                sentence_terms = set(sentence.lower().split())
                overlap_score = len(query_terms.intersection(sentence_terms))

                scored_sentences.append(
                    {
                        "sentence": sentence.strip(),
                        "score": overlap_score,
                    }
                )

            scored_sentences = sorted(
                scored_sentences,
                key=lambda item: item["score"],
                reverse=True,
            )

            selected_sentences = [
                item["sentence"]
                for item in scored_sentences[:max_sentences_per_context]
                if item["sentence"]
            ]

            compressed_text = ". ".join(selected_sentences)

            if compressed_text and not compressed_text.endswith("."):
                compressed_text += "."

            compressed_context = context.copy()
            compressed_context["text"] = compressed_text
            compressed_contexts.append(compressed_context)

        return compressed_contexts


context_service = ContextService()