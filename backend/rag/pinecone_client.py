from __future__ import annotations

from pinecone import Pinecone, ServerlessSpec

from utils.config import settings


class PineconeVectorStore:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key=settings.pinecone_api_key) if settings.pinecone_api_key else None
        self.index_name = settings.pinecone_index

        if self.pc and self.index_name not in [idx.name for idx in self.pc.list_indexes()]:
            self.pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
            )

    def upsert(self, vectors: list[tuple[str, list[float], dict]]) -> None:
        if not self.pc:
            return
        self.pc.Index(self.index_name).upsert(vectors=vectors)

    def query(self, vector: list[float], top_k: int = 5) -> list[dict]:
        if not self.pc:
            return []
        response = self.pc.Index(self.index_name).query(vector=vector, top_k=top_k, include_metadata=True)
        return response.get("matches", [])
