# ClinIQ AI

ClinIQ AI is a production-style AI healthcare platform for AI-assisted clinical reasoning, symptom analysis, disease ranking, treatment recommendation, and medical summary generation using RAG + multi-agent orchestration.

## Key Features

- Patient symptom intake with structured profile inputs.
- BioBERT/HuggingFace-based clinical entity extraction.
- RAG retrieval architecture with Pinecone + sentence-transformers embeddings.
- LangGraph multi-agent diagnosis workflow:
  - Symptom Analysis Agent
  - Medical Knowledge Retrieval Agent
  - Disease Ranking Agent
  - Risk Assessment Agent
  - Treatment Recommendation Agent
  - Clinical Summary Agent
- PDF report upload and extraction.
- Real-time Next.js dashboard with charts and agent trace.
- Dockerized full stack (backend, frontend, postgres, redis).
- CI pipeline with GitHub Actions.

## Medical Disclaimer

**This system is AI-assisted and not a substitute for professional medical advice.**

## Architecture

![Architecture Diagram Placeholder](docs/architecture-diagram-placeholder.png)

### Monorepo Structure

```text
cliniq-ai/
├── backend/
├── frontend/
├── datasets/
├── docker/
├── scripts/
├── docs/
└── infra/
```

## Backend APIs

Base URL: `http://localhost:8000/api/v1`

- `POST /analyze-symptoms`
- `POST /diagnose`
- `POST /upload-report`
- `POST /retrieve-medical-context`
- `POST /generate-summary`
- `POST /agent-trace`
- `GET /health`

Swagger docs: `http://localhost:8000/docs`

## Setup

### 1) Clone and create env

```bash
cp backend/.env.example backend/.env
```

Add required keys (`OPENAI_API_KEY`, `PINECONE_API_KEY`) for full cloud mode.

### 2) Run with Docker

```bash
docker-compose up --build
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000`

### 3) Local backend run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4) Local frontend run

```bash
cd frontend
npm install
npm run dev
```

## Dataset Generation

Generate synthetic records:

```bash
python scripts/generate_synthetic_data.py
```

Output: `datasets/synthetic_patient_records.csv` (5,000 rows)

## Real Dataset Pipeline (Symptom2Disease)

```bash
python scripts/load_medical_datasets.py --source "datasets/Symptom2Disease.csv" --out "datasets/raw/symptom2disease_raw.csv"
python scripts/preprocess_clinical_records.py --input "datasets/raw/symptom2disease_raw.csv" --output "datasets/processed/clinical_records.csv"
```

Normalized schema in `datasets/processed/clinical_records.csv`:

- `symptoms`
- `diagnosis`
- `medications`
- `notes`
- `source`

## RAG Ingestion Workflow

```bash
cd backend
python -m rag.ingest --source-dir ../datasets/processed --batch-size 32
```

Supports TXT/PDF/CSV input and stores metadata-rich chunks in Pinecone (`source`, `disease`, `chunk_id`, `section`).

## Classifier Training and Evaluation

```bash
python scripts/train_disease_classifier.py --input datasets/processed/clinical_records.csv --model-dir backend/models
python scripts/evaluate_classifier.py --input datasets/processed/clinical_records.csv --model-dir backend/models
python scripts/evaluate_rag.py --input datasets/processed/clinical_records.csv --top-k 5
python scripts/benchmark_latency.py --base-url http://127.0.0.1:8000/api/v1 --runs 5
```

Detailed docs:

- `docs/architecture.md`
- `docs/pipeline.md`
- `docs/evaluation.md`
- `docs/benchmarks.md`

## Deployment

### Railway

- Create service for backend with root path `backend` and start command:
  - `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Create service for frontend with root path `frontend` and start command:
  - `npm run start`
- Provision PostgreSQL and Redis plugins.
- Set environment variables from `.env.example`.

### Render

- Backend web service:
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Frontend web service:
  - Build: `npm install && npm run build`
  - Start: `npm run start`
- Add managed PostgreSQL and Redis.

## Security and Compliance Notes

- Input validation via Pydantic schemas.
- File type restrictions for upload endpoint.
- Environment-based secrets management.
- HIPAA-aware architectural baseline:
  - avoid storing PHI by default
  - support encrypted transport and restricted storage in production

## Analytics Captured

- Diagnosis frequency
- Symptom prevalence
- Retrieval latency
- Agent execution trace
- Confidence distribution

## Screenshots

- Dashboard placeholder: `docs/dashboard-placeholder.png`
- Agent trace placeholder: `docs/agent-trace-placeholder.png`

## Testing

```bash
cd backend
pytest -q
```

## Future Improvements

- Calibrated confidence scoring with uncertainty quantification.
- Full EHR/FHIR integration.
- Human-in-the-loop physician validation workflows.
- Region-specific guideline tuning.
- Fine-tuned medical LLM adapters.
