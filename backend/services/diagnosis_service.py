from __future__ import annotations

import time

from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential

from graphs.diagnosis_graph import build_diagnosis_graph
from models.schemas import AnalyzeSymptomsResponse, ClinicalSummary, DiagnoseResponse, ExtractedEntities, PatientInput
from services.analytics_service import AnalyticsService
from services.cache_service import CacheService
from nlp.biobert_extractor import extract_entities
from rag.retriever import MedicalRetriever


class DiagnosisService:
    def __init__(self) -> None:
        self.graph = build_diagnosis_graph()
        self.retriever = MedicalRetriever()
        self.analytics = AnalyticsService()
        self.cache = CacheService()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, min=0.2, max=1.5))
    def _retrieve_context(self, query: str) -> list[dict]:
        return self.retriever.retrieve(query, top_k=5)

    async def analyze_symptoms(self, payload: PatientInput) -> AnalyzeSymptomsResponse:
        entities = extract_entities(payload.symptoms_text)
        return AnalyzeSymptomsResponse(extracted_entities=entities, normalized_text=payload.symptoms_text.lower().strip())

    async def diagnose(self, payload: PatientInput, db: AsyncSession | None = None) -> DiagnoseResponse:
        started = time.perf_counter()
        payload_dict = payload.model_dump()
        cached = self.cache.get_json("diagnose", payload_dict)
        if cached:
            return DiagnoseResponse(**cached)

        entities: ExtractedEntities = extract_entities(payload.symptoms_text)
        retrieval_started = time.perf_counter()
        retrieval_context = self._retrieve_context(payload.symptoms_text)
        retrieval_latency_ms = (time.perf_counter() - retrieval_started) * 1000
        final_state = self.graph.invoke(
            {
                "patient_input": payload_dict,
                "extracted_entities": entities.model_dump(),
                "retrieval_context": retrieval_context,
                "agent_trace": [],
            }
        )
        summary = ClinicalSummary(**final_state["clinical_summary"])
        total_ms = (time.perf_counter() - started) * 1000
        disease_ranking = final_state.get("disease_ranking", [])
        self.analytics.track(
            top_diseases=[item["disease"] for item in disease_ranking],
            symptoms=entities.symptoms,
            retrieval_latency_ms=retrieval_latency_ms,
            execution_time_ms=total_ms,
            confidences=[item["confidence"] for item in disease_ranking],
        )
        if db and disease_ranking:
            try:
                await self.analytics.persist(
                    session=db,
                    top_disease=disease_ranking[0]["disease"],
                    symptom_count=len(entities.symptoms),
                    retrieval_latency_ms=retrieval_latency_ms,
                    execution_time_ms=total_ms,
                    confidences=[item["confidence"] for item in disease_ranking],
                )
            except Exception:
                # Degrade gracefully if DB is unavailable.
                pass

        response = DiagnoseResponse(
            disease_ranking=disease_ranking,
            summary=summary,
            agent_trace=final_state.get("agent_trace", []),
            retrieval_context=retrieval_context,
        )
        self.cache.set_json("diagnose", payload_dict, response.model_dump())
        return response
