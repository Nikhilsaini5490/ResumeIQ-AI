import re
from typing import Iterable


def normalize_whitespace(text: str) -> str:
    text = text.replace("\x00", " ")
    return re.sub(r"[ \t\r\f\v]+", " ", text).strip()


def normalize_for_match(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\-/ ]+", " ", text)
    return normalize_whitespace(text)


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalize_whitespace(text)) if s.strip()]


def split_chunks(text: str, max_words: int = 90, overlap: int = 15) -> list[str]:
    words = normalize_whitespace(text).split()
    if not words:
        return []
    chunks: list[str] = []
    step = max(1, max_words - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + max_words]).strip()
        if chunk:
            chunks.append(chunk)
        if start + max_words >= len(words):
            break
    return chunks


def unique_preserve(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(item.strip())
    return out
