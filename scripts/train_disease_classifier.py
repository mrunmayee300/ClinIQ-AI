import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder


def train(input_csv: Path, model_dir: Path, test_size: float = 0.2, random_state: int = 42) -> dict:
    df = pd.read_csv(input_csv)
    if "symptoms" not in df.columns or "diagnosis" not in df.columns:
        raise ValueError("Input CSV must contain symptoms and diagnosis columns.")
    df = df.dropna(subset=["symptoms", "diagnosis"]).copy()
    df["symptoms"] = df["symptoms"].astype(str)
    df["diagnosis"] = df["diagnosis"].astype(str)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["diagnosis"])
    X_train, X_test, y_train, y_test = train_test_split(
        df["symptoms"], y, test_size=test_size, random_state=random_state, stratify=y
    )

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=20000)),
            ("clf", LogisticRegression(max_iter=400)),
        ]
    )
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision_weighted": float(precision_score(y_test, preds, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, preds, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, preds, average="weighted", zero_division=0)),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
    }

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_dir / "disease_classifier.joblib")
    joblib.dump(label_encoder, model_dir / "label_encoder.joblib")
    (model_dir / "classifier_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train disease classifier on processed symptom dataset.")
    parser.add_argument("--input", default="datasets/processed/clinical_records.csv")
    parser.add_argument("--model-dir", default="backend/models")
    args = parser.parse_args()

    metrics = train(Path(args.input), Path(args.model_dir))
    print("[train] completed")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
