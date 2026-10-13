import requests
import polyline

def get_route(start_coords, end_coords):
    base_url = "http://router.project-osrm.org/route/v1/driving/"
    
    start = f"{start_coords[1]},{start_coords[0]}"
    end = f"{end_coords[1]},{end_coords[0]}"
    
    # Request up to 3 alternative routes with additional parameters
    url = f"{base_url}{start};{end}?overview=full&alternatives=3&steps=true&geometries=polyline&continue_straight=false"
    
    response = requests.get(url)
    data = response.json()

    routes = []

    for route in data["routes"]:
        geometry = polyline.decode(route["geometry"])
        distance = route["distance"] / 1000  # meters → km
        duration = route["duration"] / 60    # seconds → minutes

        routes.append({
            "geometry": geometry,
            "distance": distance,
            "duration": duration
        })

    return routes