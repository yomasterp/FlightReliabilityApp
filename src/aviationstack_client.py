import requests

from .config import AVIATIONSTACK_API_KEY, BASE_URL


class AviationstackClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or AVIATIONSTACK_API_KEY
        if not self.api_key:
            raise ValueError("AVIATIONSTACK_API_KEY is not set. "
                             "Set it in your .env file.")

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        params = params or {}
        params["access_key"] = self.api_key

        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    def get_flights(self, **params) -> dict:
        """
        Basic wrapper for the /v1/flights endpoint.

        Example:
            client.get_flights(limit=10)
            client.get_flights(airline_iata="UA", limit=50)
        """
        return self._get("flights", params=params)

