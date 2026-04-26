from pathlib import Path

from scripts.evaluate_classifier import evaluate


if __name__ == "__main__":
    print(evaluate(Path("datasets/processed/clinical_records.csv"), Path("backend/models")))
