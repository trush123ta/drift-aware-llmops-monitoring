from typing import Dict, List

from app.core.config import settings
from indexing.text_cleaner import clean_text, is_noisy_chunk


def chunk_text(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP,
) -> List[str]:
    """
    Splits text into smaller overlapping chunks.

    Smaller overlapping chunks improve retrieval precision for specific concepts
    such as faithfulness, recursive retrieval, and adaptive retrieval.
    """
    cleaned_text = clean_text(text)

    if len(cleaned_text) <= chunk_size:
        return [cleaned_text]

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = start + chunk_size
        chunk = cleaned_text[start:end]

        # Try not to cut in the middle of a sentence
        last_period = chunk.rfind(".")
        if last_period > chunk_size * 0.5:
            chunk = chunk[: last_period + 1]
            end = start + last_period + 1

        chunks.append(chunk.strip())

        start = max(end - chunk_overlap, start + 1)

    return chunks


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    all_chunks = []
    seen_texts = set()

    for document in documents:
        chunks = chunk_text(document["text"])

        for chunk_index, chunk in enumerate(chunks):
            cleaned_chunk = clean_text(chunk)

            if is_noisy_chunk(cleaned_chunk):
                continue

            normalized_text = cleaned_chunk.lower().strip()

            if normalized_text in seen_texts:
                continue

            seen_texts.add(normalized_text)

            chunk_id = (
                f"{document['source']}"
                f"_p{document['page'] if document['page'] else 'na'}"
                f"_c{chunk_index}"
            )

            all_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": cleaned_chunk,
                    "source": document["source"],
                    "source_type": document["source_type"],
                    "page": document["page"],
                    "chunk_index": chunk_index,
                }
            )

    return all_chunks