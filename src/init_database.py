from .database import Base, engine
from . import models  # Registers Flight on Base.metadata
from .schema_upgrade import apply_schema_patches, verify_content_hash_index


def init_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    apply_schema_patches(engine)
    if not verify_content_hash_index(engine):
        raise RuntimeError(
            "Index ux_flights_content_hash is missing after migrations. "
            "If you use Supabase, run this once with the direct connection (port 5432), "
            "or run the SQL in schema_upgrade.py from the Supabase SQL editor, then retry."
        )
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()


