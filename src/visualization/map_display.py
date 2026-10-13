import folium

def create_map(start_coords, routes, best_route_index):
    m = folium.Map(location=start_coords, zoom_start=12)

    for i, route in enumerate(routes):
        if i == best_route_index:
            color = "green"
            weight = 7
        else:
            color = "red"
            weight = 4

        folium.PolyLine(
            route["geometry"],
            color=color,
            weight=weight,
            opacity=0.8
        ).add_to(m)

    return m