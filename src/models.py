from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, Integer, String, text

from .database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    flight_date = Column(String, nullable=True, index=True)

    flight_iata = Column(String, index=True)
    airline_iata = Column(String, index=True)

    departure_airport = Column(String)
    departure_airport_iata = Column(String)
    arrival_airport = Column(String)
    arrival_airport_iata = Column(String)

    scheduled_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)

    flight_status = Column(String, index=True)

    airline_name = Column(String)

    departure_delay = Column(Integer)
    arrival_delay = Column(Integer)

    departure_terminal = Column(String)
    arrival_terminal = Column(String)
    departure_gate = Column(String)
    arrival_gate = Column(String)

    ingested_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    content_hash = Column(String(64), nullable=True)

    __table_args__ = (
        Index(
            "ux_flights_content_hash",
            "content_hash",
            unique=True,
            postgresql_where=text("content_hash IS NOT NULL"),
        ),
    )
