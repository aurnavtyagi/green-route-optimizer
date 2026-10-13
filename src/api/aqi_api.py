import requests
from src.config.settings import AQICN_API_TOKEN


def get_aqi_data(lat, lon):
    """
    Fetch real-time AQI data from AQICN for Delhi
    Returns AQI and pollutants from nearest monitoring station
    
    AQICN has 15+ stations across Delhi:
    - Anand Vihar, RK Puram, Mandir Marg, Punjabi Bagh
    - ITO, Nehru Nagar, Dwarka, Rohini, etc.
    
    Permanently free: 1000 requests/day
    """
    
    if not AQICN_API_TOKEN:
        return None

    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={AQICN_API_TOKEN}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok":
                station = data["data"]
                
                aqi = station.get("aqi", None)
                
                # Extract individual pollutants
                iaqi = station.get("iaqi", {})
                
                pm25 = iaqi.get("pm25", {}).get("v", None)
                pm10 = iaqi.get("pm10", {}).get("v", None)
                co = iaqi.get("co", {}).get("v", None)
                no2 = iaqi.get("no2", {}).get("v", None)
                so2 = iaqi.get("so2", {}).get("v", None)
                ozone = iaqi.get("o3", {}).get("v", None)
                
                # Station info
                station_name = station.get("city", {}).get("name", "Delhi")
                
                return {
                    "aqi": aqi,
                    "pm25": pm25,
                    "pm10": pm10,
                    "co": co,
                    "no2": no2,
                    "so2": so2,
                    "ozone": ozone,
                    "station": station_name
                }
        
        return None
        
    except Exception as e:
        print(f"AQICN API Error: {str(e)}")
        return None


def aqi_to_congestion_adjustment(aqi):
    """
    Convert AQI to congestion adjustment factor
    High pollution often correlates with traffic congestion
    
    AQI Categories (US EPA Standard):
    0-50: Good
    51-100: Moderate
    101-150: Unhealthy for sensitive groups
    151-200: Unhealthy
    201-300: Very Unhealthy
    301+: Hazardous
    """
    
    if aqi is None:
        return 0.0
    
    if aqi <= 50:
        return 0.0  # Good air quality, no impact
    elif aqi <= 100:
        return 0.05  # Moderate
    elif aqi <= 150:
        return 0.10  # Unhealthy for sensitive groups
    elif aqi <= 200:
        return 0.15  # Unhealthy
    elif aqi <= 300:
        return 0.25  # Very unhealthy
    else:
        return 0.35  # Hazardous


def get_aqi_category(aqi):
    """
    Returns AQI category and health message
    """
    
    if aqi is None:
        return "Unknown", "AQI data unavailable"
    
    if aqi <= 50:
        return "Good", "Air quality is satisfactory"
    elif aqi <= 100:
        return "Moderate", "Air quality is acceptable"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Sensitive people should reduce outdoor activity"
    elif aqi <= 200:
        return "Unhealthy", "Everyone may experience health effects"
    elif aqi <= 300:
        return "Very Unhealthy", "Health alert - avoid outdoor activities"
    else:
        return "Hazardous", "Emergency conditions - stay indoors"
