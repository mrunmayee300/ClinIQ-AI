import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from rag.retriever import MedicalRetriever


def evaluate(input_csv: Path, top_k: int = 5) -> dict:
    retriever = MedicalRetriever()
    df = pd.read_csv(input_csv).dropna(subset=["symptoms", "diagnosis"]).head(200)
    hits = 0
    reciprocal_ranks = []
    for _, row in df.iterrows():
        expected = str(row["diagnosis"]).lower().strip()
        matches = retriever.retrieve(str(row["symptoms"]), top_k=top_k)
        rank = None
        for idx, match in enumerate(matches, start=1):
            disease = str(match.get("disease", "")).lower().strip()
            if disease == expected:
                hits += 1
                rank = idx
                break
        reciprocal_ranks.append(1 / rank if rank else 0.0)

    total = len(df)
    return {
        "samples": total,
        f"recall_at_{top_k}": float(hits / total) if total else 0.0,
        "mrr": float(sum(reciprocal_ranks) / total) if total else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="datasets/processed/clinical_records.csv")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--out", default="docs/evaluation_rag.json")
    args = parser.parse_args()

    metrics = evaluate(Path(args.input), top_k=args.top_k)
    Path(args.out).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
