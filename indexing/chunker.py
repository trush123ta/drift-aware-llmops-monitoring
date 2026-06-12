from typing import Dict, List

from app.core.config import settings
from indexing.text_cleaner import clean_text, is_noisy_chunk


def chunk_text(text: str, chunk_size: int = settings.CHUNK_SIZE) -> List[str]:
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

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

            # prevent duplicate chunks from repeated headers/footers/pages
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