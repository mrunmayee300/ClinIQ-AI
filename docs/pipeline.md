# Pipeline

1. Load and preprocess Symptom2Disease records into `datasets/processed/clinical_records.csv`.
2. Train classifier and save artifacts:
   - `backend/models/disease_classifier.joblib`
   - `backend/models/label_encoder.joblib`
3. Ingest processed records into Pinecone using `backend/rag/ingest.py`.
4. Run diagnosis:
   - BioBERT entity extraction
   - retrieval of medical context
   - classifier-backed disease ranking (fallback to rules)
   - risk and treatment recommendation
   - final clinical summary generation
