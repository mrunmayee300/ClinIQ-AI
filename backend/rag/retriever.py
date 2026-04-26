from __future__ import annotations

from embeddings.embedder import MedicalEmbedder
from rag.pinecone_client import PineconeVectorStore


class MedicalRetriever:
    def __init__(self) -> None:
        self.embedder = MedicalEmbedder()
        self.vector_store = PineconeVectorStore()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        vector = self.embedder.embed([query])[0]
        matches = self.vector_store.query(vector=vector, top_k=top_k)
        return [
            {
                "id": m.get("id", ""),
                "score": m.get("score", 0.0),
                "text": m.get("metadata", {}).get("text", ""),
                "source": m.get("metadata", {}).get("source", "unknown"),
                "disease": m.get("metadata", {}).get("disease", "unknown"),
                "chunk_id": m.get("metadata", {}).get("chunk_id", ""),
                "section": m.get("metadata", {}).get("section", "unknown"),
            }
            for m in matches
        ]
