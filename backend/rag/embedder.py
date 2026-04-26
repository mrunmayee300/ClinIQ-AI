from __future__ import annotations

from embeddings.embedder import MedicalEmbedder


def get_embedder(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> MedicalEmbedder:
    return MedicalEmbedder(model_name=model_name)
