# Flight Reliability & Availability Tracker

Collects flight observations from the **Aviationstack** API into **PostgreSQL** (including **[Supabase](https://supabase.com/)**). Each row gets a deterministic **`content_hash`** so identical API snapshots are not stored twice, which keeps history usable for later analytics and ML.

---

## Project overview

The focus is airline on-time behavior, delays, availability patterns, and features for future reliability modeling.

---

## Prerequisites

- **Python 3.10+**
- **PostgreSQL** database reachable from your machine, or a **Supabase** project (hosted Postgres)
- **Aviationstack API key** ([aviationstack.com](https://aviationstack.com/))

---

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then edit — see “Database configuration” below
```

Create tables and apply idempotent Postgres patches (unique index on `content_hash`, columns, etc.):

```bash
python -m src.init_database
```

Patches only (safe to re-run):

```bash
python -m src.schema_upgrade
```

---

## Database configuration (local Postgres or Supabase)

Configuration is loaded from **`.env`** via **`src/config.py`**. Choose **one** primary style:

| Style | When to use |
|--------|-------------|
| **`SQLALCHEMY_DATABASE_URL`** | Recommended for **Supabase**: paste the **URI** from **Project Settings → Database** in the Supabase dashboard. The app normalizes `postgres://` / `postgresql://` URLs for SQLAlchemy + `psycopg2`. |
| **`DATABASE_URL`** | Some hosts set only this; it is used if `SQLALCHEMY_DATABASE_URL` is unset. |
| **`DB_HOST`**, **`DB_PORT`**, **`DB_NAME`**, **`DB_USER`**, **`DB_PASSWORD`** | Fine for local dev. Non-local hosts get **`sslmode=require`** unless you set **`DB_SSLMODE`**. |

**Supabase-specific notes**

- **Migrations** (`init_database`, `schema_upgrade`): prefer the **direct database** connection (**port 5432**) so `CREATE UNIQUE INDEX` runs reliably. The **transaction pooler** (**port 6543**) can block or complicate DDL; if index creation fails, run the **SQL** from `src/schema_upgrade.py` once in the **Supabase SQL Editor**, or switch to **5432** for that command only.
- **`main.py`** will try to apply patches if the deduplication index is missing, then fail with a clear message if the database still cannot create it.
- Optional **`DB_SSLMODE`** is merged into the URL when not already present (e.g. `require`, `verify-full`).

See **`.env.example`** for all variables.

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

Scheduled: runs once at startup, then every **8 hours**:

```bash
python scheduler.py
```

Details: [SCHEDULER_GUIDE.md](SCHEDULER_GUIDE.md).

---

## Read API (optional)

```bash
uvicorn src.api_main:app --reload --host 0.0.0.0 --port 8000
```

- **`GET /health`** — liveness
- **`GET /stats/observations`** — row count in `flights` (requires DB)

---

## Troubleshooting

| Symptom | What to try |
|---------|--------------|
| **`role "postgres" does not exist`** (localhost) | Your OS Postgres user is often not `postgres`. Set **`DB_USER`** to your real role, or use Supabase and a full URI. |
| **`no unique or exclusion constraint matching the ON CONFLICT`** | The unique index on **`content_hash`** is missing. Run **`python -m src.schema_upgrade`** using **direct 5432**, or run the index DDL from `schema_upgrade.py` in Supabase SQL Editor. |
| **`python` not found** | On macOS use **`python3`** or **`./venv/bin/python`** after activating **`venv`**. |

New to the stack? See [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md).
