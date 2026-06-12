import re


NOISY_KEYWORDS = [
    "references",
    "bibliography",
    "arxiv:",
    "doi.org",
    "proceedings of",
]


def clean_text(text: str) -> str:
    text = text.replace("-\n", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_noisy_chunk(text: str) -> bool:
    lower_text = text.lower()

    if len(text.strip()) < 100:
        return True

    keyword_hits = sum(keyword in lower_text for keyword in NOISY_KEYWORDS)

    if keyword_hits >= 2:
        return True

    citation_like_count = len(re.findall(r"\[\d+\]|\(\d{4}\)", text))

    if citation_like_count > 10:
        return True

    return False