from __future__ import annotations

import uuid
from typing import Optional

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class RAGStore:

    def __init__(self):

        # Embedding model
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # Persistent ChromaDB
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="translations"
        )

    # --------------------------------------------------

    def add_document(
        self,
        original: str,
        translation: str,
        metadata: Optional[dict] = None,
    ):

        text = f"{original}\n{translation}"

        embedding = self.model.encode(text).tolist()

        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
        )

    # --------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):

        if self.size == 0:
            return []

        query_embedding = self.model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        retrieved = []

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        for doc, meta in zip(docs, metas):

            retrieved.append(
                {
                    "text": doc,
                    "metadata": meta,
                }
            )

        return retrieved

    # --------------------------------------------------

    def clear(self):

        self.client.delete_collection(
            "translations"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="translations"
            )
        )

    # --------------------------------------------------

    @property
    def size(self):

        return self.collection.count()
