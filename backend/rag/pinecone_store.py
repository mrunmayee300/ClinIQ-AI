from __future__ import annotations

from .pinecone_client import PineconeVectorStore


def get_store() -> PineconeVectorStore:
    return PineconeVectorStore()
