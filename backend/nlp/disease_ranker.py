from __future__ import annotations

from models.schemas import DiseaseRank
from services.classifier_service import ClassifierService


class DiseaseRanker:
    def __init__(self) -> None:
        self.classifier = ClassifierService()

    def rank(self, text: str, top_k: int = 5) -> list[dict]:
        predictions = self.classifier.predict(text, top_k=top_k)
        return [
            DiseaseRank(
                disease=item["disease"],
                confidence=item["confidence"],
                reasoning=item.get("reasoning", "Model-based probability score."),
            ).model_dump()
            for item in predictions
        ]
