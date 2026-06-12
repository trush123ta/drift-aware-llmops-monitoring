from typing import Any, Dict, List

import requests

from app.core.config import settings


class GenerationService:
    def _format_contexts(self, retrieved_contexts: List[Dict[str, Any]]) -> str:
        formatted_contexts = []

        total_chars = 0

        for index, context in enumerate(retrieved_contexts, start=1):
            source = context.get("source", "unknown")
            page = context.get("page")
            chunk_id = context.get("chunk_id", "unknown")
            text = context.get("text", "")

            citation = f"[Source {index}: {source}"
            if page is not None:
                citation += f", page {page}"
            citation += f", chunk {chunk_id}]"

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

Answer the user question using only the provided context.
If the context is insufficient, say that the available context is not enough.
Keep the answer concise and technical.
Include source citations using the format [Source 1], [Source 2], etc.

User question:
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
                        "temperature": 0.2,
                        "top_p": 0.9,
                    },
                },
                timeout=120,
            )
            response.raise_for_status()

            return response.json()["response"].strip()

        except requests.RequestException as error:
            return (
                "Local LLM generation failed. "
                f"Reason: {str(error)}"
            )


generation_service = GenerationService()