from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    
    # IDs
    flight_iata = Column(String, index=True)
    airline_iata = Column(String, index=True)
    airline_iata = Column(String)

    
    # Route IDs
    departure_airport = Column(String)
    departure_airport_iata = Column(String)
    arrival_airport = Column(String)
    arrival_airport_iata = Column(String)

    
    # Timestamp IDs
    scheduled_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)


    # Status
    flight_status = Column(String, index=True)


    # Airline Name
    airline_name = Column(String)


    # Delays, in minutes
    departure_delay = Column(Integer)
    arrival_delay = Column(Integer)


    # Terminals & Gates
    departure_terminal = Column(String)
    arrival_terminal = Column(String)
    departure_gate = Column(String)
    arrival_gate = Column(String)


    # Flight Metadata
    ingested_at = Column(DateTime, default=datetime.utcnow)