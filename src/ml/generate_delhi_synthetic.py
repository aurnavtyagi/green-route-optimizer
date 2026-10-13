import pandas as pd
import numpy as np
import random


def generate_delhi_dataset(n_samples=15000):

    data = []

    road_types = [
        "national_highway",
        "ring_road",
        "arterial",
        "local",
        "service_lane"
    ]

    for _ in range(n_samples):

        distance_km = round(np.random.uniform(2, 45), 2)
        road_type = random.choice(road_types)

        lane_count = random.randint(1, 6)
        num_signals = random.randint(0, 20)

        hour = random.randint(0, 23)
        day_of_week = random.randint(0, 6)

        is_weekend = 1 if day_of_week >= 5 else 0
        is_peak_hour = 1 if (8 <= hour <= 11 or 17 <= hour <= 21) else 0

        temperature_c = round(np.random.uniform(5, 45), 1)
        rainfall_mm = round(np.random.exponential(4), 2)
        humidity = round(np.random.uniform(30, 95), 1)

        visibility_km = round(np.random.uniform(0.5, 10), 2)
        pollution_index = round(np.random.uniform(50, 450), 1)

        congestion_score = 1.0

        if road_type == "local":
            congestion_score += 0.25
        elif road_type == "arterial":
            congestion_score += 0.15
        elif road_type == "service_lane":
            congestion_score += 0.30

        if is_peak_hour:
            congestion_score += 0.35

        if rainfall_mm > 10:
            congestion_score += 0.3

        if visibility_km < 2:
            congestion_score += 0.3

        if pollution_index > 300:
            congestion_score += 0.15

        congestion_score += num_signals * 0.01
        congestion_score += np.random.normal(0, 0.08)

        congestion_score = round(np.clip(congestion_score, 0.8, 2.0), 2)

        avg_speed = round(55 / congestion_score, 2)
        traffic_density = round(congestion_score * 35, 2)

        data.append([
            distance_km, road_type, lane_count, num_signals,
            hour, day_of_week, is_peak_hour, is_weekend,
            temperature_c, rainfall_mm, humidity,
            visibility_km, pollution_index,
            avg_speed, traffic_density, congestion_score
        ])

    columns = [
        "distance_km", "road_type", "lane_count", "num_signals",
        "hour", "day_of_week", "is_peak_hour", "is_weekend",
        "temperature_c", "rainfall_mm", "humidity",
        "visibility_km", "pollution_index",
        "avg_speed", "traffic_density", "congestion_score"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    df = generate_delhi_dataset()
    df.to_csv("data/raw/delhi_synthetic.csv", index=False)
    print("Delhi synthetic dataset generated.")