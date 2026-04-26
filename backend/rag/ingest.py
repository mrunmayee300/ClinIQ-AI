from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from .chunker import chunk_text
from .embedder import get_embedder
from .loader import load_documents
from .pinecone_store import get_store


def _chunk_id(source: str, idx: int, chunk: str) -> str:
    digest = hashlib.sha1(f"{source}:{idx}:{chunk}".encode("utf-8")).hexdigest()
    return f"chunk-{digest}"


def ingest_documents(source_dir: str, batch_size: int = 64) -> int:
    embedder = get_embedder()
    store = get_store()
    docs = load_documents(source_dir)
    if not docs:
        return 0

    pending_vectors: list[tuple[str, list[float], dict]] = []
    processed_docs = 0

    for doc in docs:
        chunks = chunk_text(doc["text"], chunk_size=500, overlap=100)
        if not chunks:
            continue
        embeddings = embedder.embed(chunks)
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = _chunk_id(doc["source"], idx, chunk)
            pending_vectors.append(
                (
                    vector_id,
                    embedding,
                    {
                        "text": chunk,
                        "source": doc["source"],
                        "disease": doc.get("disease", "unknown"),
                        "chunk_id": vector_id,
                        "section": doc.get("section", "unknown"),
                    },
                )
            )
            if len(pending_vectors) >= batch_size:
                store.upsert(pending_vectors)
                pending_vectors.clear()
        processed_docs += 1
        if processed_docs % 100 == 0:
            print(f"[ingest] processed {processed_docs} documents...")

    if pending_vectors:
        store.upsert(pending_vectors)
    return processed_docs


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest medical corpus into Pinecone.")
    parser.add_argument("--source-dir", default="datasets/processed", help="Directory containing txt/pdf/csv medical files.")
    parser.add_argument("--batch-size", type=int, default=64, help="Upsert batch size.")
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    print(f"[ingest] loading documents from {source_dir}")
    count = ingest_documents(str(source_dir), batch_size=args.batch_size)
    print(f"[ingest] completed ingestion for {count} documents")


if __name__ == "__main__":
    main()
