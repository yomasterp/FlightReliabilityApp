"""
Deterministic hashing of Aviationstack flight payloads for deduplicated inserts.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_flight_observation(api_flight: dict[str, Any]) -> dict[str, Any]:
    """
    Projection of provider fields used for uniqueness and downstream ML labeling.
    Order is reconstructed via JSON sort_keys; values are primitives / nested dicts only.
    """
    airline = api_flight.get("airline") or {}
    flight_info = api_flight.get("flight") or {}
    departure = api_flight.get("departure") or {}
    arrival = api_flight.get("arrival") or {}

    return {
        "airline_iata": airline.get("iata"),
        "airline_name": airline.get("name"),
        "arrival_airport": arrival.get("airport"),
        "arrival_airport_iata": arrival.get("iata"),
        "arrival_delay": arrival.get("delay"),
        "arrival_gate": arrival.get("gate"),
        "arrival_scheduled": arrival.get("scheduled"),
        "arrival_actual": arrival.get("actual"),
        "arrival_terminal": arrival.get("terminal"),
        "departure_airport": departure.get("airport"),
        "departure_airport_iata": departure.get("iata"),
        "departure_delay": departure.get("delay"),
        "departure_gate": departure.get("gate"),
        "departure_scheduled": departure.get("scheduled"),
        "departure_actual": departure.get("actual"),
        "departure_terminal": departure.get("terminal"),
        "flight_date": api_flight.get("flight_date"),
        "flight_iata": flight_info.get("iata"),
        "flight_number": flight_info.get("number"),
        "flight_status": api_flight.get("flight_status"),
    }


def observation_content_hash(api_flight: dict[str, Any]) -> str:
    """SHA-256 fingerprint of canonical observation (stable duplicate detection)."""
    blob = canonical_flight_observation(api_flight)
    payload = json.dumps(blob, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
