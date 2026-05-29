from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import init_db, list_tables
from api import brands, personas, feed, ads, events, optimization
from api import context as context_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Contextual Ad Engine", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brands.router)
app.include_router(personas.router)
app.include_router(feed.router)
app.include_router(ads.router)
app.include_router(events.router)
app.include_router(optimization.router)
app.include_router(context_router.router)

# Serve uploaded images as static files
_uploads = Path(__file__).parent / "uploads"
_uploads.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads)), name="uploads")


@app.get("/health")
def health():
    return {"status": "ok", "database": "connected", "tables": list_tables()}
