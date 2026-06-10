from pathlib import Path


def retrieve_documents(query: str):

    kb_path = Path("data/knowledge_base.txt")

    with open(kb_path, "r", encoding="utf-8") as f:
        documents = f.read().split("\n")

    results = []

    for doc in documents:

        if query.lower() in doc.lower():
            results.append(doc)

    return results