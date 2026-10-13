# src/emission/emission_calculator.py

def get_base_emission(vehicle_type: str) -> float:
    """
    Returns base emission (grams CO2 per km) 
    based on vehicle type.
    """
    emission_factors = {
        "petrol": 120,
        "diesel": 140,
        "cng": 100,
        "ev": 20
    }

    return emission_factors.get(vehicle_type.lower(), 120)


def calculate_emission(distance_km: float, vehicle_type: str, congestion_factor: float = 1.2) -> dict:
    """
    Calculates total carbon emission for a route.

    Parameters:
    - distance_km: Route distance in kilometers
    - vehicle_type: petrol/diesel/cng/ev
    - congestion_factor: Multiplier for traffic impact (temporary static)

    Returns:
    - Dictionary with grams and kilograms of CO2
    """

    base_emission = get_base_emission(vehicle_type)

    emission_grams = distance_km * base_emission * congestion_factor
    emission_kg = emission_grams / 1000

    return {
        "grams": round(emission_grams, 2),
        "kilograms": round(emission_kg, 3)
    }