# Project Structure Explanation

This document explains the layout of the Flight Reliability & Availability Tracker repository.

## Root Directory Files

### `tests/`
- **Purpose**: `pytest` tests for parsing, hashing, and the FastAPI health route (no live Postgres required for most tests)
- **Note**: `httpx` is required for `TestClient`

### `.env.example`
- **Purpose**: Documents environment variables — copy to **`.env`** locally (never commit secrets)
- **Contents**: Aviationstack settings; database via **`SQLALCHEMY_DATABASE_URL`** / **`DATABASE_URL`** or **`DB_*`**; optional **`DB_SSLMODE`**; notes for **Supabase** (direct **5432** vs pooler **6543** for migrations)

### `pytest.ini`
- **Purpose**: Registers `tests/` and sets `pythonpath` to the project root

### `README.md`
- **Purpose**: Overview, setup, **Supabase** / Postgres configuration, ingestion, API, troubleshooting

### `requirements.txt`
- **Purpose**: Python dependencies, including:
  - `requests`, `python-dotenv`, `sqlalchemy`, `psycopg2-binary`
  - `schedule` — periodic collection
  - `fastapi`, `uvicorn` — read API (`src/api_main.py`)
  - `pytest`, `httpx` — tests
  - `pandas`, `scikit-learn` — reserved for future analytics (not used in `src/` ingestion path yet)

### `.gitignore`
- **Purpose**: Excludes `.env`, `venv/`, logs, caches, local data files

### `scheduler.py`
- **Purpose**: Runs **`src.main.main()`** once at startup, then every **8 hours**
- **Usage**: `python scheduler.py` from project root (with **`venv`** activated or **`./venv/bin/python`**)

### `SCHEDULER_GUIDE.md`
- **Purpose**: Scheduler behavior, interval customization, logging

### `BEGINNER_GUIDE.md`
- **Purpose**: Conceptual walkthrough for newcomers (API, Postgres/Supabase, files, basic commands)

## Source Directory (`src/`)

### `src/__init__.py`
- **Purpose**: Marks `src` as a Python package

### `src/config.py`
- **Purpose**: Loads **`.env`**, builds **`SQLALCHEMY_DATABASE_URL`**
- **Resolution order**: **`SQLALCHEMY_DATABASE_URL`** → else **`DATABASE_URL`** → else individual **`DB_*`**
- **Notable behavior**:
  - Normalizes `postgres://` / plain `postgresql://` to **`postgresql+psycopg2://`**
  - URL-encodes username/password for special characters
  - Appends **`sslmode=require`** for non-local **`DB_HOST`** unless **`DB_SSLMODE`** or `sslmode` is already in the URL

### `src/aviationstack_client.py`
- **Purpose**: **`AviationstackClient`** — authenticated GETs to Aviationstack (`get_flights`, etc.)

### `src/database.py`
- **Purpose**: SQLAlchemy **`engine`**, **`SessionLocal`**, declarative **`Base`**

### `src/models.py`
- **Purpose**: **`Flight`** ORM model (`flights` table) — route, times, delays, **`flight_date`**, **`content_hash`**, **`ingested_at`** (UTC, timezone-aware)
- **Uniqueness**: Unique index **`ux_flights_content_hash`** on **`content_hash`** supports **`INSERT … ON CONFLICT DO NOTHING`**

### `src/flight_snapshot.py`
- **Purpose**: Canonical JSON projection + **`observation_content_hash()`** (SHA-256) for deduplication

### `src/schema_upgrade.py`
- **Purpose**: Idempotent DDL — adds columns if needed, **`ingested_at`** timestamptz migration when applicable, **`DROP`/`CREATE UNIQUE INDEX`** on **`public.flights(content_hash)`**
- **Usage**: **`python -m src.schema_upgrade`**; also invoked from **`init_database`** and **retry path in `main`** when the index is missing

### `src/api_main.py`
- **Purpose**: Minimal FastAPI app — **`/health`**, **`/stats/observations`**

### `src/init_database.py`
- **Purpose**: **`create_all`**, then **`apply_schema_patches`**, then verifies the **`content_hash`** index exists

### `src/main.py`
- **Purpose**: Fetches flights, maps rows, bulk insert with **`ON CONFLICT (content_hash) DO NOTHING`**

## Data Flow

1. **`scheduler.py`** (optional) triggers collection every **8 hours**
2. **`src/main.py`** calls Aviationstack and inserts into Postgres
3. **`src/database.py`** / **`src/models.py`** persist rows; duplicates skipped by **`content_hash`**

## Setup Checklist

1. **`pip install -r requirements.txt`** (ideally in a **`venv`**)
2. **`.env`** with **`AVIATIONSTACK_API_KEY`** and database settings (see **`.env.example`**; **Supabase** users: paste URI or **`DB_HOST=db.<ref>.supabase.co`**)
3. **`python -m src.init_database`** (use **direct 5432** URI for Supabase if pooler causes DDL issues)
4. **`python -m src.main`** to verify ingestion
5. **`python scheduler.py`** for scheduled runs

## Future Enhancements

- Analytics / aggregates in Python or SQL
- Richer FastAPI routes
- Modeling (the repo already lists **`pandas`** / **`scikit-learn`** for future work)
