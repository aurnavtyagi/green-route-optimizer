import streamlit as st
import streamlit.components.v1 as components

from src.routing.geocoder import get_coordinates
from src.routing.route_fetcher import get_route
from src.visualization.map_display import create_map
from src.emission.emission_calculator import calculate_emission
from src.api.weather_api import get_weather_data, weather_to_congestion_adjustment
from src.api.aqi_api import AQICN_API_TOKEN, get_aqi_data, aqi_to_congestion_adjustment, get_aqi_category


st.set_page_config(page_title="Delhi AI Green Route", layout="wide")

st.title("Delhi AI Green Route Optimization")
st.markdown("Find the lowest carbon emission route based on traffic & weather conditions.")

if not AQICN_API_TOKEN:
    st.warning(
        "AQI is disabled because AQICN_API_TOKEN is not set. "
        "Set AQICN_API_TOKEN in .env or Streamlit secrets, then restart Streamlit."
    )

# -------------------------------
# User Inputs
# -------------------------------

start_location = st.text_input("Enter Start Location (Delhi)")
end_location = st.text_input("Enter End Location (Delhi)")

vehicle_type = st.selectbox(
    "Select Vehicle Type",
    ["petrol", "diesel", "cng", "ev"]
)

# -------------------------------
# Main Button
# -------------------------------

if st.button("Find Green Route"):

    # Input validation
    if not start_location or not end_location:
        st.error("Please enter both start and end locations.")
        st.stop()

    # -------------------------------
    # Geocoding
    # -------------------------------
    try:
        start_coords = get_coordinates(start_location)
        end_coords = get_coordinates(end_location)
    except Exception as e:
        st.error(f"Geocoding Error: {str(e)}")
        st.stop()

    # -------------------------------
    # Fetch Routes
    # -------------------------------
    try:
        routes = get_route(start_coords, end_coords)
        if not routes:
            st.error("No routes found between these locations.")
            st.stop()
    except Exception as e:
        st.error(f"Routing Error: {str(e)}")
        st.stop()

    # -------------------------------
    # Get Weather Data (Open-Meteo)
    # -------------------------------
    try:
        temp, rain, visibility = get_weather_data(start_coords[0], start_coords[1])
        weather_adjustment = weather_to_congestion_adjustment(temp, rain, visibility)
    except Exception:
        temp, rain, visibility = None, None, None
        weather_adjustment = 0

    # -------------------------------
    # Get AQI Data for Start Location
    # -------------------------------
    try:
        start_aqi_data = get_aqi_data(start_coords[0], start_coords[1])
        if start_aqi_data:
            start_aqi = start_aqi_data["aqi"]
            aqi_adjustment = aqi_to_congestion_adjustment(start_aqi)
            start_aqi_category, start_aqi_message = get_aqi_category(start_aqi)
        else:
            start_aqi, aqi_adjustment = None, 0
            start_aqi_category, start_aqi_message = "Unknown", "AQI data unavailable"
    except Exception:
        start_aqi, aqi_adjustment = None, 0
        start_aqi_category, start_aqi_message = "Unknown", "AQI data unavailable"

    # -------------------------------
    # Get AQI Data for End Location
    # -------------------------------
    try:
        end_aqi_data = get_aqi_data(end_coords[0], end_coords[1])
        if end_aqi_data:
            end_aqi = end_aqi_data["aqi"]
            end_aqi_category, end_aqi_message = get_aqi_category(end_aqi)
        else:
            end_aqi = None
            end_aqi_category, end_aqi_message = "Unknown", "AQI data unavailable"
    except Exception:
        end_aqi = None
        end_aqi_category, end_aqi_message = "Unknown", "AQI data unavailable"

    emissions = []

    # -------------------------------
    # Emission Calculation
    # -------------------------------
    for route in routes:

        try:
            # Avoid divide-by-zero
            if route["duration"] <= 0:
                avg_speed = 1
            else:
                avg_speed = route["distance"] / (route["duration"] / 60)

            base_congestion = max(1.0, 60 / max(avg_speed, 1))

            final_congestion = base_congestion + weather_adjustment + aqi_adjustment

            emission_data = calculate_emission(
                distance_km=route["distance"],
                vehicle_type=vehicle_type,
                congestion_factor=final_congestion
            )

            route["emission"] = emission_data["kilograms"]
            emissions.append(route["emission"])

        except Exception:
            route["emission"] = float("inf")
            emissions.append(float("inf"))

    if not emissions:
        st.error("Emission calculation failed.")
        st.stop()

    best_route_index = emissions.index(min(emissions))

    # -------------------------------
    # Display Map
    # -------------------------------
    route_map = create_map(start_coords, routes, best_route_index)
    components.html(route_map._repr_html_(), height=600)

    # -------------------------------
    # Weather & AQI Display
    # -------------------------------
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weather Conditions (Start Location)")
        if temp is not None:
            st.write(f"Temperature: {temp} °C")
            st.write(f"Rain: {rain} mm")
            st.write(f"Visibility: {visibility} m")
        else:
            st.write("Weather data unavailable.")
    
    with col2:
        st.subheader("Air Quality Index")
        
        st.write("**Start Location:**")
        if start_aqi is not None:
            st.write(f"AQI: {start_aqi}")
            st.write(f"Category: {start_aqi_category}")
            st.write(f"Impact: {start_aqi_message}")
            if start_aqi_data:
                st.write(f"Station: {start_aqi_data.get('station', 'N/A')}")
                if start_aqi_data.get('pm25'):
                    st.write(f"PM2.5: {start_aqi_data['pm25']} µg/m³")
        else:
            st.write("AQI data unavailable.")
        
        st.write("")
        st.write("**End Location:**")
        if end_aqi is not None:
            st.write(f"AQI: {end_aqi}")
            st.write(f"Category: {end_aqi_category}")
            st.write(f"Impact: {end_aqi_message}")
            if end_aqi_data:
                st.write(f"Station: {end_aqi_data.get('station', 'N/A')}")
                if end_aqi_data.get('pm25'):
                    st.write(f"PM2.5: {end_aqi_data['pm25']} µg/m³")
        else:
            st.write("AQI data unavailable.")

    # -------------------------------
    # Route Comparison
    # -------------------------------
    st.subheader("Route Comparison")

    for i, route in enumerate(routes):
        if i == best_route_index:
            st.success(
                f"Route {i+1} (Recommended - Lowest Emission)\n\n"
                f"Distance: {route['distance']:.2f} km\n\n"
                f"Duration: {route['duration']:.2f} min\n\n"
                f"Emission: {route['emission']:.3f} kg CO₂"
            )
        else:
            st.write(
                f"Route {i+1}\n\n"
                f"Distance: {route['distance']:.2f} km\n\n"
                f"Duration: {route['duration']:.2f} min\n\n"
                f"Emission: {route['emission']:.3f} kg CO₂"
            )