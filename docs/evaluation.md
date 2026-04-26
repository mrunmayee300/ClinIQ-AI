# Evaluation

## Classifier

Run:

```bash
python scripts/train_disease_classifier.py --input datasets/processed/clinical_records.csv --model-dir backend/models
python scripts/evaluate_classifier.py --input datasets/processed/clinical_records.csv --model-dir backend/models
```

Reported metrics:

- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1 (weighted)

Latest local run (`datasets/processed/clinical_records.csv`):

- Accuracy: `0.9610`
- Precision (weighted): `0.9656`
- Recall (weighted): `0.9610`
- F1 (weighted): `0.9604`

## RAG Retrieval

Run:

```bash
cd backend
python -m rag.ingest --source-dir ../datasets/processed --batch-size 32
cd ..
python scripts/evaluate_rag.py --input datasets/processed/clinical_records.csv --top-k 5
```

Reported metrics:

- Recall@K
- MRR

Latest local run before Pinecone re-ingestion:

- Recall@5: `0.0000`
- MRR: `0.0000`
