import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from .config import CLIP_EMBEDDING_DIM, FAISS_INDEX_PATH, FAISS_METADATA_PATH, VECTOR_DB_DIR


class VectorStore:
    def __init__(self) -> None:
        self.index_path: Path = FAISS_INDEX_PATH
        self.metadata_path: Path = FAISS_METADATA_PATH

        VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

        self.index = self._load_or_create_index()
        self.records = self._load_records()

    def _load_or_create_index(self) -> faiss.Index:
        if self.index_path.exists():
            return faiss.read_index(str(self.index_path))

        # Use inner-product on L2-normalized vectors, equivalent to cosine similarity.
        return faiss.IndexFlatIP(CLIP_EMBEDDING_DIM)

    def _load_records(self) -> list[dict[str, Any]]:
        if self.metadata_path.exists():
            return json.loads(self.metadata_path.read_text())
        return []

    def _persist(self) -> None:
        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.records, indent=2))

    def add_embedding(self, embedding: np.ndarray, metadata: dict[str, Any]) -> None:
        vector = self._normalize(embedding).reshape(1, -1)
        self.index.add(vector.astype(np.float32))
        self.records.append(metadata)
        self._persist()

    def search_embedding(self, query_embedding: np.ndarray, top_k: int = 3) -> list[dict[str, Any]]:
        if self.index.ntotal == 0:
            return []

        query = self._normalize(query_embedding).reshape(1, -1).astype(np.float32)
        k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(query, k)
        results: list[dict[str, Any]] = []

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            metadata = self.records[idx] if idx < len(self.records) else {}
            results.append(
                {
                    "id": int(idx),
                    "score": float(score),
                    "metadata": metadata,
                }
            )

        return results

    def get_stats(self) -> dict[str, Any]:
        return {
            "index_path": str(self.index_path),
            "metadata_path": str(self.metadata_path),
            "vector_count": int(self.index.ntotal),
            "metadata_count": len(self.records),
            "dimension": CLIP_EMBEDDING_DIM,
        }

    def get_records(self, limit: int = 10) -> list[dict[str, Any]]:
        safe_limit = max(0, min(limit, len(self.records)))
        return self.records[:safe_limit]

    @staticmethod
    def _normalize(vector: np.ndarray) -> np.ndarray:
        vector = vector.astype(np.float32)
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
