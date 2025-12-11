from .aviationstack_client import AviationstackClient


def main():
    client = AviationstackClient()

    # Keep it small at first so you don't hit rate limits
    params = {
        "limit": 5
        # You can add filters here later:
        # "airline_iata": "UA",
        # "flight_status": "active",
    }

    print("Fetching flights from Aviationstack...")
    data = client.get_flights(**params)

    flights = data.get("data", [])
    print(f"Received {len(flights)} flights")

    # Print some basic info for the first few flights
    for idx, flight in enumerate(flights, start=1):
        airline = flight.get("airline", {}) or {}
        flight_info = flight.get("flight", {}) or {}
        departure = flight.get("departure", {}) or {}
        arrival = flight.get("arrival", {}) or {}

        print(f"\nFlight #{idx}")
        print(f"  Airline: {airline.get('name')} ({airline.get('iata')})")
        print(f"  Flight: {flight_info.get('iata')}")
        print(f"  From: {departure.get('airport')} ({departure.get('iata')})")
        print(f"  To:   {arrival.get('airport')} ({arrival.get('iata')})")
        print(f"  Status: {flight.get('flight_status')}")


if __name__ == "__main__":
    main()

