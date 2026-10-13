"""
GeoJSON Visualizer for Delhi Traffic Dataset
Visualizes road network, probe counts, and infrastructure features
"""

import json
import folium
from folium import plugins
import os


def load_geojson(file_path):
    """Load GeoJSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def visualize_road_network(geojson_file, output_html="map_output.html"):
    """
    Visualize road network from probe count GeoJSON
    Shows hourly traffic data for specific date
    """
    
    print(f"Loading: {geojson_file}")
    data = load_geojson(geojson_file)
    
    # Create map centered on Delhi
    m = folium.Map(
        location=[28.6139, 77.2090],  # Delhi coordinates
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add GeoJSON layer
    # Check if features have properties
    has_properties = (len(data['features']) > 0 and 
                     'properties' in data['features'][0] and 
                     len(data['features'][0]['properties']) > 0)
    
    if has_properties:
        # Get available fields from first feature
        prop_keys = list(data['features'][0]['properties'].keys())[:3]  # First 3 properties
        
        folium.GeoJson(
            data,
            name="Delhi Road Network",
            style_function=lambda x: {
                'color': 'blue',
                'weight': 2,
                'opacity': 0.6
            },
            tooltip=folium.GeoJsonTooltip(
                fields=prop_keys,
                aliases=[f"{k}:" for k in prop_keys],
                style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
            )
        ).add_to(m)
    else:
        folium.GeoJson(
            data,
            name="Delhi Road Network",
            style_function=lambda x: {
                'color': 'blue',
                'weight': 2,
                'opacity': 0.6
            }
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen option
    plugins.Fullscreen().add_to(m)
    
    # Save map
    m.save(output_html)
    print(f"Map saved to: {output_html}")
    print(f"Total features: {len(data['features'])}")
    
    return m


def visualize_facilities(facilities_json, output_html="facilities_map.html"):
    """
    Visualize infrastructure facilities (schools, hospitals, etc.)
    """
    
    print(f"Loading: {facilities_json}")
    data = load_geojson(facilities_json)
    
    # Create map centered on Delhi
    m = folium.Map(
        location=[28.6139, 77.2090],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Color mapping for different facility types
    colors = {
        'education': 'blue',
        'healthcare': 'red',
        'retail': 'green',
        'government': 'purple',
        'entertainment': 'orange',
        'religious': 'pink',
        'transport': 'darkblue',
        'leisure': 'lightgreen',
        'mixed': 'gray',
        'historic': 'brown'
    }
    
    # Add facilities with colored markers
    if 'features' in data:
        for feature in data['features']:
            if feature['geometry']['type'] == 'Point':
                coords = feature['geometry']['coordinates']
                props = feature.get('properties', {})
                facility_type = props.get('category', 'unknown').lower()
                
                folium.CircleMarker(
                    location=[coords[1], coords[0]],  # Note: GeoJSON is [lon, lat]
                    radius=5,
                    color=colors.get(facility_type, 'gray'),
                    fill=True,
                    fillColor=colors.get(facility_type, 'gray'),
                    fillOpacity=0.6,
                    popup=f"{props.get('name', 'Unknown')}<br>Type: {facility_type}"
                ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    plugins.Fullscreen().add_to(m)
    
    # Save map
    m.save(output_html)
    print(f"Facilities map saved to: {output_html}")
    
    return m


def visualize_delhi_boundary(geojson_file, output_html="delhi_boundary.html"):
    """
    Visualize Delhi administrative boundaries
    """
    
    print(f"Loading: {geojson_file}")
    data = load_geojson(geojson_file)
    
    # Create map
    m = folium.Map(
        location=[28.6139, 77.2090],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add boundary
    folium.GeoJson(
        data,
        name="Delhi Boundary",
        style_function=lambda x: {
            'fillColor': 'lightblue',
            'color': 'darkblue',
            'weight': 3,
            'fillOpacity': 0.2
        }
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    plugins.Fullscreen().add_to(m)
    
    m.save(output_html)
    print(f"Boundary map saved to: {output_html}")
    
    return m


def main():
    """Main function to visualize different GeoJSON files"""
    
    base_path = "data/raw/new_delhi_traffic_dataset"
    
    print("=" * 60)
    print("Delhi Traffic GeoJSON Visualizer")
    print("=" * 60)
    
    # Menu
    print("\nSelect what to visualize:")
    print("1. Delhi Administrative Boundary")
    print("2. Infrastructure Facilities")
    print("3. Road Network (Probe Counts - specific date)")
    print("4. All of the above")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1" or choice == "4":
        print("\n--- Visualizing Delhi Boundary ---")
        boundary_file = os.path.join(base_path, "geojson", "new_delhi.json")
        if os.path.exists(boundary_file):
            visualize_delhi_boundary(boundary_file)
        else:
            print(f"File not found: {boundary_file}")
    
    if choice == "2" or choice == "4":
        print("\n--- Visualizing Facilities ---")
        facilities_file = os.path.join(base_path, "facility", "features_geopkg.json")
        if os.path.exists(facilities_file):
            visualize_facilities(facilities_file)
        else:
            print(f"File not found: {facilities_file}")
    
    if choice == "3" or choice == "4":
        print("\n--- Visualizing Road Network (Probe Counts) ---")
        
        # List available dates
        probe_dir = os.path.join(base_path, "probe_counts", "geojson")
        if os.path.exists(probe_dir):
            files = [f for f in os.listdir(probe_dir) if f.endswith('.geojson')]
            
            if files:
                print(f"\nAvailable dates ({len(files)} files):")
                for i, f in enumerate(files[:5], 1):
                    print(f"{i}. {f}")
                if len(files) > 5:
                    print(f"... and {len(files) - 5} more files")
                
                # Use first file as example
                probe_file = os.path.join(probe_dir, files[0])
                print(f"\nVisualizing: {files[0]}")
                print("(Note: Large file - may take a moment to load)")
                
                visualize_road_network(probe_file, "delhi_roads_probe_count.html")
            else:
                print("No probe count files found")
        else:
            print(f"Directory not found: {probe_dir}")
    
    print("\n" + "=" * 60)
    print("Visualization complete!")
    print("Open the generated HTML files in your browser to view maps.")
    print("=" * 60)


if __name__ == "__main__":
    main()
