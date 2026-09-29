from functools import lru_cache
from typing import Sequence
import numpy as np

from app.config import get_settings


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._model = None
        self.available = False
        if self.settings.use_embeddings:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.settings.embedding_model)
                self.available = True
            except Exception:
                self._model = None
                self.available = False

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        if not self.available or self._model is None:
            raise RuntimeError("Transformer embeddings are unavailable")
        return self._model.encode(list(texts), normalize_embeddings=True)


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
