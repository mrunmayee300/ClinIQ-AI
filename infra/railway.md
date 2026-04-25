# Railway Deployment Notes

## Backend Service

- Root directory: `backend`
- Install command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Frontend Service

- Root directory: `frontend`
- Install command: `npm install`
- Build command: `npm run build`
- Start command: `npm run start`

## Required Environment Variables

- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_INDEX`
- `PINECONE_CLOUD`
- `PINECONE_REGION`
- `POSTGRES_DSN`
- `REDIS_URL`
- `JWT_SECRET`
- `NEXT_PUBLIC_API_BASE`
