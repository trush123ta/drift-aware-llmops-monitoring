from typing import Any, Dict, List


class SourceService:
    def build_sources(
        self,
        retrieved_contexts: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        sources = []

        for index, context in enumerate(retrieved_contexts, start=1):
            sources.append(
                {
                    "source_id": f"S{index}",
                    "source": context.get("source"),
                    "source_type": context.get("source_type"),
                    "page": context.get("page"),
                    "chunk_id": context.get("chunk_id"),
                    "distance": context.get("distance"),
                }
            )

        return sources


source_service = SourceService()