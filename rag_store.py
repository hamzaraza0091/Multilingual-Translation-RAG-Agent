from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    id: str
    text: str
    embedding: np.ndarray
    metadata: dict = field(default_factory=dict)


class RAGStore:

    def __init__(self, chunk_size: int = 120, overlap: int = 30):
        self.chunks: list[Chunk] = []
        self.chunk_size = chunk_size
        self.overlap = overlap

        # FREE LOCAL EMBEDDING MODEL
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # ─────────────────────────────

    def _split_chunks(self, text: str) -> list[str]:
        words = text.split()

        chunks = []
        i = 0

        while i < len(words):
            chunk = " ".join(
                words[i:i + self.chunk_size]
            )

            chunks.append(chunk)

            i += self.chunk_size - self.overlap

        return chunks

    # ─────────────────────────────

    @staticmethod
    def _cosine(a, b):
        return np.dot(a, b) / (
            np.linalg.norm(a) *
            np.linalg.norm(b)
        )

    # ─────────────────────────────

    def add_document(
        self,
        original: str,
        translation: str,
        metadata: Optional[dict] = None,
    ):

        combined = f"{original}\n{translation}"

        raw_chunks = self._split_chunks(combined)

        added = 0

        for text in raw_chunks:

            embedding = self.model.encode(text)

            self.chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    text=text,
                    embedding=embedding,
                    metadata=metadata or {},
                )
            )

            added += 1

        return added

    # ─────────────────────────────

    def retrieve(self, query: str, top_k: int = 3):

        if not self.chunks:
            return []

        query_embedding = self.model.encode(query)

        scored = []

        for chunk in self.chunks:

            score = self._cosine(
                query_embedding,
                chunk.embedding
            )

            scored.append({
                "text": chunk.text,
                "score": float(score),
                "metadata": chunk.metadata,
            })

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scored[:top_k]

    # ─────────────────────────────

    def clear(self):
        self.chunks.clear()

    @property
    def size(self):
        return len(self.chunks)