from __future__ import annotations
import json
import urllib.request
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import get_settings
from app.services.embeddings import get_embedding_service
from app.utils.text import split_chunks


@dataclass
class Chunk:
    text: str
    source: str


class ResumeRAG:
    def __init__(self, resume_text: str, job_text: str):
        self.settings = get_settings()
        self.chunks: list[Chunk] = [Chunk(c, "resume") for c in split_chunks(resume_text)] + [Chunk(c, "job") for c in split_chunks(job_text)]

    def retrieve(self, query: str, k: int = 5) -> list[Chunk]:
        if not self.chunks:
            return []
        service = get_embedding_service()
        if service.available:
            texts = [c.text for c in self.chunks]
            vecs = service.encode(texts)
            q = service.encode([query])[0]
            scores = vecs @ q
        else:
            vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            mat = vec.fit_transform([c.text for c in self.chunks] + [query])
            scores = cosine_similarity(mat[:-1], mat[-1:]).ravel()
        idx = np.argsort(scores)[::-1][:k]
        return [self.chunks[i] for i in idx]

    def answer(self, query: str, context_k: int = 5) -> str:
        context = self.retrieve(query, context_k)
        context_text = "\n\n".join(f"[{c.source}] {c.text}" for c in context)
        if self.settings.use_ollama:
            prompt = (
                "You are a placement interview assistant. Use ONLY the supplied resume/job context. "
                "Do not invent facts. Give concise, practical answers.\n\n"
                f"CONTEXT:\n{context_text}\n\nQUESTION:\n{query}\n"
            )
            try:
                data = json.dumps({"model": self.settings.ollama_model, "prompt": prompt, "stream": False}).encode("utf-8")
                req = urllib.request.Request(self.settings.ollama_url, data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                return payload.get("response", "").strip() or self.fallback(query, context)
            except Exception:
                pass
        return self.fallback(query, context)

    @staticmethod
    def fallback(query: str, context: list[Chunk]) -> str:
        q = query.lower()
        if "question" in q or "interview" in q:
            topics = []
            for c in context:
                if "project" in c.text.lower():
                    topics.append("Explain one project in detail, including architecture, trade-offs and measurable results.")
                if "python" in c.text.lower():
                    topics.append("Which Python libraries did you use, and why were they appropriate?")
                if "machine learning" in c.text.lower() or "xgboost" in c.text.lower():
                    topics.append("How did you evaluate the ML model and handle class imbalance or threshold selection?")
                if "fastapi" in c.text.lower():
                    topics.append("How did you expose the model as an API and what would you change for production scale?")
            topics.extend([
                "Which skill in the job description is currently your biggest gap?",
                "How would you improve one project if you had two more weeks?"
            ])
            return "\n".join(f"{i+1}. {t}" for i, t in enumerate(dict.fromkeys(topics)))
        return "Relevant context retrieved:\n" + "\n".join(f"- {c.text}" for c in context[:3])
