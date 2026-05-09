"""
Idempotent DDL for existing PostgreSQL deployments (additive columns / indexes).

Run after `python -m src.init_database` or call `apply_schema_patches(engine)` programmatically.
"""

from __future__ import annotations

from sqlalchemy import Engine, text

PATCHES_SQL = """
ALTER TABLE flights ADD COLUMN IF NOT EXISTS flight_date VARCHAR;
ALTER TABLE flights ADD COLUMN IF NOT EXISTS content_hash VARCHAR(64);

DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'flights'
      AND column_name = 'ingested_at'
      AND data_type = 'timestamp without time zone'
  ) THEN
    ALTER TABLE flights
      ALTER COLUMN ingested_at TYPE TIMESTAMPTZ
      USING ingested_at AT TIME ZONE 'UTC';
  END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS ux_flights_content_hash
ON flights (content_hash)
WHERE content_hash IS NOT NULL;
"""


def apply_schema_patches(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(PATCHES_SQL))


if __name__ == "__main__":
    from .database import engine

    print("Applying schema patches...")
    apply_schema_patches(engine)
    print("Done.")
