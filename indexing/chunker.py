from typing import Dict, List


CHUNK_SIZE = 700


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]

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

    for document in documents:
        chunks = chunk_text(document["text"])

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = (
                f"{document['source']}"
                f"_p{document['page'] if document['page'] else 'na'}"
                f"_c{chunk_index}"
            )

            all_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "source": document["source"],
                    "source_type": document["source_type"],
                    "page": document["page"],
                    "chunk_index": chunk_index,
                }
            )

    return all_chunks