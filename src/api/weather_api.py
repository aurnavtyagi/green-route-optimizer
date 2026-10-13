import requests
import datetime


def get_weather_data(lat, lon):
    """
    Fetch current hour weather data from Open-Meteo
    """

    now = datetime.datetime.utcnow().hour

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&hourly=temperature_2m,rain,visibility"
        f"&forecast_days=1"
    )

    response = requests.get(url).json()

    if "hourly" in response:
        temperature = response["hourly"]["temperature_2m"][now]
        rain = response["hourly"]["rain"][now]
        visibility = response["hourly"]["visibility"][now]

        return temperature, rain, visibility

    return None, None, None


def weather_to_congestion_adjustment(temp, rain, visibility):
    adjustment = 0

    # Rain impact
    if rain > 5:
        adjustment += 0.25
    elif rain > 1:
        adjustment += 0.1

    # Low visibility impact (fog/smog)
    if visibility < 2000:
        adjustment += 0.3
    elif visibility < 5000:
        adjustment += 0.1

    # Extreme temperature impact (Delhi summer)
    if temp > 40:
        adjustment += 0.05

    return adjustment