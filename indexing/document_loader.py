from pathlib import Path
from typing import Dict, List

import fitz  # PyMuPDF


RAW_DOCS_DIR = Path("data/raw_docs")
RAW_PDFS_DIR = Path("data/raw_pdfs")


def load_markdown_documents() -> List[Dict]:
    documents = []

    for file_path in RAW_DOCS_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "source_type": "markdown",
                "page": None,
                "text": text,
            }
        )

    return documents


def load_pdf_documents() -> List[Dict]:
    documents = []

    for file_path in RAW_PDFS_DIR.glob("*.pdf"):
        pdf = fitz.open(file_path)

        for page_index, page in enumerate(pdf):
            text = page.get_text().strip()

            if not text:
                continue

            documents.append(
                {
                    "source": file_path.name,
                    "source_type": "pdf",
                    "page": page_index + 1,
                    "text": text,
                }
            )

    return documents


def load_documents() -> List[Dict]:
    markdown_docs = load_markdown_documents()
    pdf_docs = load_pdf_documents()

    return markdown_docs + pdf_docs