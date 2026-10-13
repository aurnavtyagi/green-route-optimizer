from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


def get_coordinates(location_name):
    """
    Converts location name into latitude and longitude.
    Automatically biases search to Delhi, India.
    """

    if not location_name:
        raise ValueError("Location cannot be empty.")

    try:
        geolocator = Nominatim(user_agent="delhi_green_route_app")

        # Automatically bias search to Delhi, India
        query = f"{location_name}, Delhi, India"

        location = geolocator.geocode(query, timeout=10)

        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(
                "Location not found. Try a more specific place name."
            )

    except GeocoderTimedOut:
        time.sleep(1)
        raise ValueError("Geocoding service timed out. Please try again.")

    except GeocoderServiceError:
        raise ValueError("Geocoding service unavailable. Please try later.")