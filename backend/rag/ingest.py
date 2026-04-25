from __future__ import annotations

from pathlib import Path

from embeddings.embedder import MedicalEmbedder
from rag.pinecone_client import PineconeVectorStore


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start += max(chunk_size - overlap, 1)
    return chunks


def ingest_documents(source_dir: str) -> int:
    embedder = MedicalEmbedder()
    store = PineconeVectorStore()
    vectors = []
    processed = 0

    for path in Path(source_dir).glob("**/*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        chunks = chunk_text(text)
        embeddings = embedder.embed(chunks)
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append((f"{path.stem}-{idx}", embedding, {"text": chunk, "source": str(path)}))
        processed += 1

    if vectors:
        store.upsert(vectors)
    return processed
