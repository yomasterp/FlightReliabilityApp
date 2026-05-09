from .database import Base, engine
from . import models  # Registers Flight on Base.metadata
from .schema_upgrade import apply_schema_patches


def init_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    apply_schema_patches(engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()


