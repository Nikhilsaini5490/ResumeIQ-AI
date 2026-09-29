from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.embeddings import get_embedding_service


@dataclass
class SimilarityResult:
    tfidf_score: float
    embedding_score: float | None
    semantic_score: float


class MatchingService:
    @staticmethod
    def tfidf_similarity(a: str, b: str) -> float:
        if not a.strip() or not b.strip():
            return 0.0
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vec.fit_transform([a, b])
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

    @staticmethod
    def embedding_similarity(a: str, b: str) -> float | None:
        service = get_embedding_service()
        if not service.available:
            return None
        vectors = service.encode([a, b])
        score = float(np.dot(vectors[0], vectors[1]))
        return max(0.0, min(1.0, score))

    @classmethod
    def compare(cls, a: str, b: str) -> SimilarityResult:
        tfidf = cls.tfidf_similarity(a, b)
        emb = cls.embedding_similarity(a, b)
        semantic = emb if emb is not None else tfidf
        return SimilarityResult(tfidf_score=tfidf, embedding_score=emb, semantic_score=semantic)
