from pathlib import Path

from scripts.evaluate_rag import evaluate


if __name__ == "__main__":
    print(evaluate(Path("datasets/processed/clinical_records.csv"), top_k=5))
