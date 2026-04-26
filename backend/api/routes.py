from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import require_jwt
from database.session import get_session
from models.schemas import AnalyzeSymptomsResponse, DiagnoseResponse, HealthResponse, PatientInput
from rag.retriever import MedicalRetriever
from services.diagnosis_service import DiagnosisService
from services.report_service import ReportService

router = APIRouter()


@lru_cache(maxsize=1)
def get_diagnosis_service() -> DiagnosisService:
    return DiagnosisService()


@lru_cache(maxsize=1)
def get_medical_retriever() -> MedicalRetriever:
    return MedicalRetriever()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", service="cliniq-ai-backend")


@router.post("/analyze-symptoms", response_model=AnalyzeSymptomsResponse)
async def analyze_symptoms(payload: PatientInput):
    return await get_diagnosis_service().analyze_symptoms(payload)


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(payload: PatientInput, db: AsyncSession = Depends(get_session)):
    return await get_diagnosis_service().diagnose(payload, db)


@router.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf", "text/plain"}:
        raise HTTPException(status_code=400, detail="Only PDF or plain text files are allowed.")

    content = await file.read()
    text = ReportService.extract_pdf_text(content) if file.content_type == "application/pdf" else content.decode("utf-8", errors="ignore")
    return {"filename": file.filename, "extracted_text": text[:10000]}


@router.post("/retrieve-medical-context")
async def retrieve_medical_context(payload: PatientInput, db: AsyncSession = Depends(get_session)):
    retrieval_context = get_medical_retriever().retrieve(payload.symptoms_text, top_k=5)
    return {"retrieval_context": retrieval_context}


@router.post("/generate-summary")
async def generate_summary(payload: PatientInput, db: AsyncSession = Depends(get_session)):
    result = await get_diagnosis_service().diagnose(payload, db)
    return {"summary": result.summary}


@router.post("/agent-trace")
async def agent_trace(payload: PatientInput, db: AsyncSession = Depends(get_session)):
    result = await get_diagnosis_service().diagnose(payload, db)
    return {"agent_trace": result.agent_trace}


@router.get("/analytics")
async def analytics(_: dict = Depends(require_jwt), db: AsyncSession = Depends(get_session)):
    svc = get_diagnosis_service()
    return {"snapshot": svc.analytics.snapshot(), "recent_events": await svc.analytics.recent_events(db)}
