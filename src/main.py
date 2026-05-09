from datetime import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from .aviationstack_client import AviationstackClient
from .database import SessionLocal
from .flight_snapshot import observation_content_hash
from .models import Flight
from .schema_upgrade import apply_schema_patches, verify_content_hash_index


def parse_flight_data(dt_str: str | None) -> datetime | None:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def api_flight_to_row(flight: dict) -> dict:
    """Map Aviationstack flight object to ORM column dict (with content_hash)."""
    airline = flight.get("airline", {})
    flight_info = flight.get("flight", {})
    departure = flight.get("departure", {})
    arrival = flight.get("arrival", {})

    ch = observation_content_hash(flight)

    return {
        "flight_date": flight.get("flight_date"),
        "flight_iata": flight_info.get("iata"),
        "airline_iata": airline.get("iata"),
        "departure_airport": departure.get("airport"),
        "departure_airport_iata": departure.get("iata"),
        "arrival_airport": arrival.get("airport"),
        "arrival_airport_iata": arrival.get("iata"),
        "scheduled_departure": parse_flight_data(departure.get("scheduled")),
        "scheduled_arrival": parse_flight_data(arrival.get("scheduled")),
        "actual_departure": parse_flight_data(departure.get("actual")),
        "actual_arrival": parse_flight_data(arrival.get("actual")),
        "flight_status": flight.get("flight_status"),
        "airline_name": airline.get("name"),
        "departure_delay": departure.get("delay"),
        "arrival_delay": arrival.get("delay"),
        "departure_terminal": departure.get("terminal"),
        "arrival_terminal": arrival.get("terminal"),
        "departure_gate": departure.get("gate"),
        "arrival_gate": arrival.get("gate"),
        "content_hash": ch,
    }


def save_flight_data(db: Session, flights: list[dict]) -> int:
    """Insert rows; skip exact duplicate observations (same content_hash). Returns rows attempted."""
    rows = [api_flight_to_row(f) for f in flights]
    if not rows:
        return 0

    bind = db.get_bind()
    if not verify_content_hash_index(bind):
        apply_schema_patches(bind)
        if not verify_content_hash_index(bind):
            raise RuntimeError(
                "Missing unique index on flights.content_hash (needed for ON CONFLICT). "
                "Set SQLALCHEMY_DATABASE_URL to Supabase direct DB (port 5432), run: "
                "python -m src.schema_upgrade — or execute the CREATE UNIQUE INDEX block in "
                "src/schema_upgrade.py using the Supabase SQL editor."
            )

    stmt = pg_insert(Flight.__table__).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["content_hash"])
    db.execute(stmt)
    db.commit()
    return len(rows)


def main():
    client = AviationstackClient()

    params = {
        "limit": 100,
        "flight_status": "active",
    }

    print("Fetching flights from Aviationstack:")
    data = client.get_flights(**params)

    flights = data.get("data", [])
    print(f"Found {len(flights)} flights")

    if not flights:
        return

    db = SessionLocal()
    try:
        attempted = save_flight_data(db, flights)
        print(f"Processed {attempted} flight observation(s) (duplicates skipped by content_hash).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
