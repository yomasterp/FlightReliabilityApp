(MODEL IN PROGRESS)

# Flight Reliability & Availability Tracker

Uses the Aviationstack API to collect flight observations into **PostgreSQL**, with **deterministic fingerprints** (`content_hash`) so duplicate payloads are skipped—keeping history clean for downstream ML.

---

## Project overview

Collected data supports analysis of airline on-time behavior, delays, availability patterns, and predictive features. Ambition longer-term is reliability forecasting for selected airlines.

---

## Prerequisites

- Python 3.10+
- PostgreSQL reachable with credentials in `.env`

---

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edit: set AVIATIONSTACK_API_KEY and DB_* as needed
```

Create tables and apply idempotent Postgres patches:

```bash
python -m src.init_database
```

(Optional) Re-run DDL patches only:

```bash
python -m src.schema_upgrade
```

---

## Automated checks

```bash
pytest
```

---

## Running ingestion

Single run:

```bash
python -m src.main
```

Scheduled (runs once at startup, then every **8 hours**):

```bash
python scheduler.py
```

See [SCHEDULER_GUIDE.md](SCHEDULER_GUIDE.md).

---

## Read API

```bash
uvicorn src.api_main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET /health`
- Observation count: `GET /stats/observations`
