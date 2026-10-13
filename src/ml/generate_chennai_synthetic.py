import pandas as pd
import numpy as np
import random


def generate_chennai_dataset(n_samples=17000):

    data = []

    road_type_variations = [
        "highway", "Highway", "HIGHWAY", "hw",
        "arterial", "Arterial",
        "local", "local road"
    ]

    for _ in range(n_samples):

        distance_km = round(np.random.uniform(2, 40), 2)

        road_type = random.choice(road_type_variations)

        # Lane count
        lane_count = random.randint(1, 6)

        num_signals = random.randint(0, 15)

        hour = random.randint(0, 23)
        day_of_week = random.randint(0, 6)

        is_weekend = 1 if day_of_week >= 5 else 0
        is_peak_hour = 1 if (8 <= hour <= 10 or 17 <= hour <= 20) else 0

        temperature_c = round(np.random.uniform(25, 42), 1)
        rainfall_mm = round(np.random.exponential(3), 2)
        humidity = round(np.random.uniform(60, 95), 1)

        congestion_score = 1.0

        if "local" in road_type.lower():
            congestion_score += 0.2
        elif "arterial" in road_type.lower():
            congestion_score += 0.1

        if is_peak_hour:
            congestion_score += 0.3

        if rainfall_mm > 10:
            congestion_score += 0.3
        elif rainfall_mm > 3:
            congestion_score += 0.1

        congestion_score += num_signals * 0.01
        congestion_score += np.random.normal(0, 0.1)

        avg_speed = round(50 / max(congestion_score, 0.5), 2)
        traffic_density = round(congestion_score * 30, 2)

        data.append([
            distance_km, road_type, lane_count, num_signals,
            hour, day_of_week, is_peak_hour, is_weekend,
            temperature_c, rainfall_mm, humidity,
            avg_speed, traffic_density, congestion_score
        ])

    columns = [
        "distance_km", "road_type", "lane_count", "num_signals",
        "hour", "day_of_week", "is_peak_hour", "is_weekend",
        "temperature_c", "rainfall_mm", "humidity",
        "avg_speed", "traffic_density", "congestion_score"
    ]

    df = pd.DataFrame(data, columns=columns)

    # 🔴 Introduce Missing Values (5%)
    for col in ["temperature_c", "rainfall_mm", "humidity", "avg_speed"]:
        df.loc[df.sample(frac=0.05).index, col] = np.nan

    # 🔴 Introduce Outliers (1%)
    df.loc[df.sample(frac=0.01).index, "temperature_c"] = 55
    df.loc[df.sample(frac=0.01).index, "rainfall_mm"] = 150
    df.loc[df.sample(frac=0.01).index, "avg_speed"] = 120
    df.loc[df.sample(frac=0.01).index, "congestion_score"] = 2.5

    return df


if __name__ == "__main__":
    df = generate_chennai_dataset(17000)
    df.to_csv("data/raw/chennai_synthetic2.csv", index=False)
    print("Chennai synthetic dataset with irregularities generated.")