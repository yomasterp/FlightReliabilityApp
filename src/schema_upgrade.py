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

-- Full unique index (not partial) so ON CONFLICT (content_hash) matches cleanly.
-- Multiple NULLs are still allowed (Postgres NULLs-distinct semantics).
-- If migrations ran only via transaction pooler and this failed, run once in Supabase SQL editor.
DROP INDEX IF EXISTS ux_flights_content_hash;
CREATE UNIQUE INDEX ux_flights_content_hash ON public.flights (content_hash);
"""


def apply_schema_patches(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(PATCHES_SQL))


def verify_content_hash_index(engine: Engine) -> bool:
    """Return True if the unique index for content_hash exists (required for INSERT ... ON CONFLICT)."""
    stmt = text(
        """
        SELECT 1
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = 'flights'
          AND indexname = 'ux_flights_content_hash'
        """
    )
    with engine.connect() as conn:
        return conn.execute(stmt).first() is not None


if __name__ == "__main__":
    from .database import engine

    print("Applying schema patches...")
    apply_schema_patches(engine)
    print("Done.")
