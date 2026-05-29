# Contextual Ad Intelligence Engine — Bangladesh

A contextual advertising platform tailored for the Bangladeshi market, featuring two interfaces: a consumer-facing feed (Interface A) that surfaces organic content and intelligently ranked sponsored ads based on inferred user personas, and a brand management dashboard (Interface B) where brands can upload products, generate AI-optimised ad creatives, track attribution metrics, and trigger automated optimisation cycles — all backed by a FastAPI + SQLite backend with a React + Vite + Tailwind CSS frontend.

## Running locally

**Backend**
```bash
cd backend
pip3 install -r requirements.txt
python3 -m uvicorn main:app --reload
# http://localhost:8000/health
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```
