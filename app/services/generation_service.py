from typing import Any, Dict, List

import requests

from app.core.config import settings


class GenerationService:
    def _format_contexts(self, retrieved_contexts: List[Dict[str, Any]]) -> str:
        formatted_contexts = []
        total_chars = 0

        for index, context in enumerate(retrieved_contexts, start=1):
            source_id = f"S{index}"
            source = context.get("source", "unknown")
            page = context.get("page")
            text = context.get("text", "")

            citation = f"[{source_id}] {source}"
            if page is not None:
                citation += f", page {page}"

            block = f"{citation}\n{text}"

            if total_chars + len(block) > settings.MAX_CONTEXT_CHARS:
                break

            formatted_contexts.append(block)
            total_chars += len(block)

        return "\n\n".join(formatted_contexts)

    def _build_prompt(self, query: str, retrieved_contexts: List[Dict[str, Any]]) -> str:
        context_text = self._format_contexts(retrieved_contexts)

        return f"""
You are a grounded RAG assistant.

Use only the retrieved context below to answer the question.
Do not use outside knowledge.
Do not add information that is not directly supported by the context.
Prefer the highest-ranked source when it fully answers the question.
Keep the answer concise and technical.
Use citation IDs exactly like [S1], [S2], etc.
Do not cite a source unless the sentence is directly supported by that source.
Do not mention "provided context", "available context", or add meta-notes.
If the retrieved context is insufficient, say: "The retrieved context is not sufficient to answer this question."


Question:
{query}

Retrieved context:
{context_text}

Answer:
""".strip()

    def generate_answer(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
    ) -> str:
        if not retrieved_contexts:
            return "I could not find relevant context to answer this query."

        prompt = self._build_prompt(query, retrieved_contexts)

        try:
            response = requests.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "num_predict": 160,
                    },
                },
                timeout=120,
            )
            response.raise_for_status()

            return response.json()["response"].strip()

        except requests.RequestException:
            best_context = retrieved_contexts[0]["text"]
            fallback = best_context[:700].strip()

            return (
                "Local LLM generation failed, so a fallback extractive answer was returned: "
                f"{fallback}"
            )


generation_service = GenerationService()