from __future__ import annotations

from pathlib import Path

import joblib


class ClassifierService:
    def __init__(self) -> None:
        self.model = None
        self.label_encoder = None
        self.available = False
        model_dir = Path(__file__).resolve().parents[1] / "models"
        model_path = model_dir / "disease_classifier.joblib"
        encoder_path = model_dir / "label_encoder.joblib"
        if model_path.exists() and encoder_path.exists():
            self.model = joblib.load(model_path)
            self.label_encoder = joblib.load(encoder_path)
            self.available = True

    def predict(self, symptoms_text: str, top_k: int = 5) -> list[dict]:
        if not self.available or self.model is None or self.label_encoder is None:
            return []
        probabilities = self.model.predict_proba([symptoms_text])[0]
        pairs = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            {
                "disease": self.label_encoder.inverse_transform([idx])[0],
                "confidence": float(round(prob, 4)),
                "reasoning": "ML classifier confidence from symptom text vectorization.",
            }
            for idx, prob in pairs
        ]
