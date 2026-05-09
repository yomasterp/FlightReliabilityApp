import pytest

from src.main import api_flight_to_row, parse_flight_data
from src.flight_snapshot import canonical_flight_observation, observation_content_hash


def test_parse_flight_data_z_suffix():
    dt = parse_flight_data("2026-05-08T14:22:33.000Z")
    assert dt is not None
    assert dt.utcoffset().total_seconds() == 0


def test_parse_flight_data_invalid():
    assert parse_flight_data("not-a-datetime") is None


@pytest.fixture()
def sample_flight():
    return {
        "flight_date": "2026-05-08",
        "flight_status": "active",
        "airline": {"iata": "UA", "name": "United Airlines"},
        "flight": {"iata": "UA242", "number": "242"},
        "departure": {
            "airport": "SFO",
            "iata": "SFO",
            "scheduled": "2026-05-08T18:05:00+00:00",
            "terminal": "3",
            "delay": None,
            "gate": "E5",
            "actual": None,
        },
        "arrival": {
            "airport": "EWR",
            "iata": "EWR",
            "scheduled": "2026-05-09T02:30:00+00:00",
            "terminal": None,
            "delay": None,
            "gate": None,
            "actual": None,
        },
    }


def test_observation_hash_stable(sample_flight):
    h1 = observation_content_hash(sample_flight)
    h2 = observation_content_hash(sample_flight.copy())
    assert h1 == h2
    assert len(h1) == 64


def test_duplicate_observation_collapses_hash(sample_flight):
    canon = canonical_flight_observation(sample_flight)
    assert canon["flight_status"] == "active"
    dup = canonical_flight_observation(sample_flight.copy())
    assert dup == canon


def test_api_flight_row_top_level_status(sample_flight):
    row = api_flight_to_row(sample_flight)
    assert row["flight_status"] == "active"
    assert row["flight_date"] == "2026-05-08"
    assert len(row["content_hash"]) == 64
