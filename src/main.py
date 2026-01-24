from datetime import datetime
from sqlalchemy.orm import Session

from .aviationstack_client import AviationstackClient
from .database import SessionLocal
from .models import Flight


def parse_flight_data(dt_str: str | None = None) -> datetime | None:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        return None


def save_flight_data(db: Session, flights: list[dict]) -> None:
    for flight in flights:
        airline = flight.get("airline", {})
        flight_info = flight.get("flight", {})
        departure = flight.get("departure", {})
        arrival = flight.get("arrival", {})

        db_flight = Flight(
            flight_iata=flight_info.get("iata"),
            airline_iata=airline.get("iata"),
            departure_airport=departure.get("airport"),
            departure_airport_iata=departure.get("iata"),
            arrival_airport=arrival.get("airport"),
            arrival_airport_iata=arrival.get("iata"),
            scheduled_departure=parse_flight_data(departure.get("scheduled")),
            scheduled_arrival=parse_flight_data(arrival.get("scheduled")),
            actual_departure=parse_flight_data(departure.get("actual")),
            actual_arrival=parse_flight_data(arrival.get("actual")),
            flight_status=flight_info.get("status"),
        )

        db.add(db_flight)

    db.commit()


def main():
    client = AviationstackClient()

    params = {
        "limit": 20,
        # add more filters here later!!!
        # airport_iata="LAX",
        # flight_status="scheduled",
    }

    print(f"Fetching flights from Aviationstack:")
    data = client.get_flights(**params)

    flights = data.get("data", [])
    print(f"Found {len(flights)} flights")

    if not flights:
        return

    db = SessionLocal()
    try:
        save_flight_data(db, flights)
        print("Flight data saved to PostgreSQL successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()