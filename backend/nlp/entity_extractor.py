from __future__ import annotations

from functools import lru_cache

from transformers import pipeline


@lru_cache(maxsize=1)
def get_medical_ner():
    return pipeline(
        "token-classification",
        model="dmis-lab/biobert-base-cased-v1.2",
        aggregation_strategy="simple",
    )


def extract_tokens(text: str) -> list[dict]:
    return get_medical_ner()(text)
