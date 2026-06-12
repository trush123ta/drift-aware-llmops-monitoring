import re
from typing import Any, Dict, List


class ContextService:
    def _tokenize(self, text: str) -> set[str]:
        tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

        stopwords = {
            "how", "what", "why", "the", "and", "are", "for", "with",
            "that", "this", "from", "into", "does", "can", "using",
            "retrieval", "augmented", "generation",
        }

        return {token for token in tokens if token not in stopwords}

    def _split_sentences(self, text: str) -> List[str]:
        return [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
            if sentence.strip()
        ]

    def compress_contexts(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        max_sentences_per_context: int = 5,
    ) -> List[Dict[str, Any]]:
        query_terms = self._tokenize(query)
        compressed_contexts = []

        for context_rank, context in enumerate(retrieved_contexts, start=1):
            text = context.get("text", "")
            sentences = self._split_sentences(text)

            scored_sentences = []

            for sentence_index, sentence in enumerate(sentences):
                sentence_terms = self._tokenize(sentence)
                overlap_score = len(query_terms.intersection(sentence_terms))

                important_bonus = 0
                lower_sentence = sentence.lower()

                if any(
                    keyword in lower_sentence
                    for keyword in [
                        "relevance",
                        "accuracy",
                        "faithfulness",
                        "correctness",
                        "evaluates",
                        "evaluation",
                        "metrics",
                    ]
                ):
                    important_bonus += 3

                # Favor earlier/high-ranked retrieved chunks
                rank_bonus = max(0, 6 - context_rank)

                scored_sentences.append(
                    {
                        "sentence": sentence,
                        "score": overlap_score + important_bonus + rank_bonus,
                        "sentence_index": sentence_index,
                    }
                )

            scored_sentences = sorted(
                scored_sentences,
                key=lambda item: item["score"],
                reverse=True,
            )

            selected = scored_sentences[:max_sentences_per_context]

            # Restore original sentence order for readability
            selected = sorted(selected, key=lambda item: item["sentence_index"])

            selected_sentences = [item["sentence"] for item in selected]

            compressed_text = " ".join(selected_sentences).strip()

            compressed_context = context.copy()
            compressed_context["text"] = compressed_text
            compressed_contexts.append(compressed_context)

        return compressed_contexts


context_service = ContextService()