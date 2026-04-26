# ClinIQ AI Architecture

- **Input Layer**: FastAPI receives symptom payloads and reports.
- **NLP Layer**: BioBERT-based extraction in `backend/nlp/`.
- **RAG Layer**: chunking + embedding + Pinecone indexing/retrieval in `backend/rag/`.
- **Reasoning Layer**: LangGraph multi-agent orchestration in `backend/graphs/` and `backend/agents/`.
- **Model Layer**: Logistic regression classifier artifacts in `backend/models/`.
- **State Layer**: Redis cache + PostgreSQL analytics event persistence.
- **Presentation Layer**: Next.js dashboard with disease chart, trace, context, and latency.
