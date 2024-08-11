import requests
from requests.exceptions import SSLError

from config import settings
from exceptions import GeocoderServiceError


def geocode(latitude: float, longitude: float) -> dict:
    url = ("https://us1.locationiq.com/v1/reverse?format=json&normalizeaddress=1&key=" + settings.geocoder.api_key +
           f"&lat={latitude}&lon={longitude}")
    try:
        response = requests.get(url=url, timeout=10)
        if response.status_code == 200:
            data = response.json()

            details = data.get("address")
            return details
        else:
            raise GeocoderServiceError(error_message=response.json().get("error"))
    except (requests.exceptions.Timeout, SSLError):
        raise GeocoderServiceError(error_message="timed out waiting for")
