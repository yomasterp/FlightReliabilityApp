"""Minimal read-only FastAPI surface for ingestion health checks and basic counts."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Flight

app = FastAPI(title="Flight Reliability Tracker", version="0.1.0")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stats/observations")
def observation_stats(db: Session = Depends(get_db)) -> dict[str, int]:
    total = db.query(Flight).count()
    return {"flight_observations": total}
