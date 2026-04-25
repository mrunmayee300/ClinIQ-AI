from __future__ import annotations

import json
from collections import Counter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import AnalyticsEvent


class AnalyticsService:
    def __init__(self) -> None:
        self.diagnosis_frequency = Counter()
        self.symptom_frequency = Counter()
        self.retrieval_latencies_ms: list[float] = []
        self.agent_execution_times_ms: list[float] = []
        self.confidences: list[float] = []

    def track(
        self,
        top_diseases: list[str],
        symptoms: list[str],
        retrieval_latency_ms: float,
        execution_time_ms: float,
        confidences: list[float],
    ) -> None:
        self.diagnosis_frequency.update(top_diseases)
        self.symptom_frequency.update(symptoms)
        self.retrieval_latencies_ms.append(retrieval_latency_ms)
        self.agent_execution_times_ms.append(execution_time_ms)
        self.confidences.extend(confidences)

    async def persist(
        self,
        session: AsyncSession,
        top_disease: str,
        symptom_count: int,
        retrieval_latency_ms: float,
        execution_time_ms: float,
        confidences: list[float],
    ) -> None:
        event = AnalyticsEvent(
            top_disease=top_disease,
            symptom_count=symptom_count,
            retrieval_latency_ms=retrieval_latency_ms,
            execution_time_ms=execution_time_ms,
            confidence_blob=json.dumps(confidences),
        )
        session.add(event)
        await session.commit()

    async def recent_events(self, session: AsyncSession, limit: int = 20) -> list[dict]:
        rows = (await session.execute(select(AnalyticsEvent).order_by(AnalyticsEvent.id.desc()).limit(limit))).scalars().all()
        return [
            {
                "id": row.id,
                "top_disease": row.top_disease,
                "symptom_count": row.symptom_count,
                "retrieval_latency_ms": row.retrieval_latency_ms,
                "execution_time_ms": row.execution_time_ms,
                "confidence_blob": row.confidence_blob,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]

    def snapshot(self) -> dict:
        return {
            "diagnosis_frequency": dict(self.diagnosis_frequency.most_common(10)),
            "common_symptoms": dict(self.symptom_frequency.most_common(10)),
            "avg_retrieval_latency_ms": (sum(self.retrieval_latencies_ms) / len(self.retrieval_latencies_ms))
            if self.retrieval_latencies_ms
            else 0,
            "avg_agent_execution_time_ms": (sum(self.agent_execution_times_ms) / len(self.agent_execution_times_ms))
            if self.agent_execution_times_ms
            else 0,
            "confidence_distribution": self.confidences[-50:],
        }
