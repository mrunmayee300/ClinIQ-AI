import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def evaluate(input_csv: Path, model_dir: Path) -> dict:
    model = joblib.load(model_dir / "disease_classifier.joblib")
    label_encoder = joblib.load(model_dir / "label_encoder.joblib")
    df = pd.read_csv(input_csv).dropna(subset=["symptoms", "diagnosis"]).copy()
    y = label_encoder.transform(df["diagnosis"].astype(str))
    _, X_test, _, y_test = train_test_split(df["symptoms"].astype(str), y, test_size=0.2, random_state=42, stratify=y)
    preds = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision_weighted": float(precision_score(y_test, preds, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, preds, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, preds, average="weighted", zero_division=0)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="datasets/processed/clinical_records.csv")
    parser.add_argument("--model-dir", default="backend/models")
    parser.add_argument("--out", default="docs/evaluation_classifier.json")
    args = parser.parse_args()

    metrics = evaluate(Path(args.input), Path(args.model_dir))
    Path(args.out).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
