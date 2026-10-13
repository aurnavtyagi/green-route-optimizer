"""
Convert Chennai synthetic data to Delhi-specific traffic patterns
Adjusts congestion, weather, and traffic characteristics to match Delhi conditions
"""

import pandas as pd
import numpy as np

def convert_to_delhi_patterns(df):
    """
    Transform Chennai synthetic data to match Delhi traffic reality
    """
    
    print("🔄 Converting Chennai data to Delhi traffic patterns...")
    
    # Make a copy
    delhi_df = df.copy()
    
    # 1. TEMPERATURE ADJUSTMENTS (Delhi has extreme seasons)
    print("  📊 Adjusting temperature patterns...")
    # Delhi: Winter (Dec-Feb) 5-20°C, Summer (Mar-May) 25-45°C, Monsoon (Jun-Sep) 25-35°C
    # Chennai: More moderate year-round 25-40°C
    
    delhi_df['month'] = np.random.randint(1, 13, len(delhi_df))  # Add month for seasonality
    
    def adjust_temperature(row):
        month = row['month']
        base_temp = row['temperature_c']
        
        if month in [12, 1, 2]:  # Winter - colder
            return np.random.uniform(5, 20)
        elif month in [3, 4, 5]:  # Summer - hotter
            return np.random.uniform(30, 46)
        elif month in [6, 7, 8, 9]:  # Monsoon - moderate
            return np.random.uniform(25, 35)
        else:  # Autumn
            return np.random.uniform(20, 32)
    
    delhi_df['temperature_c'] = delhi_df.apply(adjust_temperature, axis=1)
    
    # 2. RAINFALL ADJUSTMENTS (Delhi has less rain, concentrated in monsoon)
    print("  🌧️ Adjusting rainfall patterns...")
    
    def adjust_rainfall(row):
        month = row['month']
        
        if month in [7, 8, 9]:  # Monsoon season - more rain
            return np.random.exponential(scale=3.0) if np.random.random() < 0.4 else 0
        elif month in [12, 1, 2]:  # Winter - occasional rain
            return np.random.exponential(scale=0.5) if np.random.random() < 0.1 else 0
        else:  # Other months - rare rain
            return np.random.exponential(scale=0.3) if np.random.random() < 0.05 else 0
    
    delhi_df['rainfall_mm'] = delhi_df.apply(adjust_rainfall, axis=1)
    
    # 3. HUMIDITY ADJUSTMENTS
    print("  💧 Adjusting humidity levels...")
    
    def adjust_humidity(row):
        month = row['month']
        
        if month in [7, 8, 9]:  # Monsoon - high humidity
            return np.random.uniform(60, 90)
        elif month in [3, 4, 5, 6]:  # Summer - moderate to low
            return np.random.uniform(30, 55)
        else:  # Winter/Autumn - moderate
            return np.random.uniform(40, 70)
    
    delhi_df['humidity'] = delhi_df.apply(adjust_humidity, axis=1)
    
    # 4. CONGESTION SCORE ADJUSTMENTS (Delhi has worse traffic!)
    print("  🚦 Adjusting congestion patterns...")
    
    # Delhi traffic multipliers
    def adjust_congestion(row):
        base_congestion = row['congestion_score']
        hour = row['hour']
        is_peak = row['is_peak_hour']
        is_weekend = row['is_weekend']
        road_type = row['road_type']
        
        # Base increase for Delhi (10-20% worse than Chennai)
        multiplier = np.random.uniform(1.1, 1.2)
        
        # Peak hours are MUCH worse in Delhi
        if is_peak == 1:
            multiplier *= 1.3
        
        # Morning peak (8-10 AM) is particularly bad
        if hour in [8, 9, 10]:
            multiplier *= 1.15
        
        # Evening peak (5-8 PM) is even worse
        if hour in [17, 18, 19, 20]:
            multiplier *= 1.25
        
        # Local roads suffer more in Delhi
        if road_type == 'local':
            multiplier *= 1.15
        
        # Weekends are slightly better
        if is_weekend == 1:
            multiplier *= 0.85
        
        # Apply multiplier
        new_congestion = base_congestion * multiplier
        
        # Cap at 3.0 (maximum congestion)
        return min(3.0, new_congestion)
    
    delhi_df['congestion_score'] = delhi_df.apply(adjust_congestion, axis=1)
    
    # 5. TRAFFIC DENSITY ADJUSTMENTS
    print("  🚗 Adjusting traffic density...")
    
    def adjust_traffic_density(row):
        if pd.isna(row['traffic_density']):
            # Fill missing values based on congestion
            return row['congestion_score'] * np.random.uniform(25, 35)
        else:
            # Increase density by 15-25% for Delhi
            return row['traffic_density'] * np.random.uniform(1.15, 1.25)
    
    delhi_df['traffic_density'] = delhi_df.apply(adjust_traffic_density, axis=1)
    
    # 6. AVERAGE SPEED ADJUSTMENTS (lower speeds in Delhi)
    print("  🏎️ Adjusting average speeds...")
    
    def adjust_speed(row):
        if pd.isna(row['avg_speed']):
            # Derive from congestion score
            # Congestion 1.0 = 50 km/h, 3.0 = 15 km/h
            base_speed = 50 - (row['congestion_score'] - 1.0) * 17.5
            return max(10, base_speed + np.random.uniform(-5, 5))
        else:
            # Reduce speeds by 10-20% for Delhi
            reduction = np.random.uniform(0.80, 0.90)
            return row['avg_speed'] * reduction
    
    delhi_df['avg_speed'] = delhi_df.apply(adjust_speed, axis=1)
    
    # 7. ROAD TYPE DISTRIBUTION (Delhi-specific)
    print("  🛣️ Adjusting road type distribution...")
    
    # Delhi has more highways and expressways
    road_type_mapping = {
        'local': ['local', 'residential', 'service'],
        'hw': ['highway', 'expressway', 'arterial'],
        'arterial': ['arterial', 'main_road', 'highway']
    }
    
    # 20% chance to upgrade road type for Delhi's better infrastructure
    def upgrade_road_type(road_type):
        if np.random.random() < 0.2:
            if road_type == 'local':
                return 'arterial'
            elif road_type == 'arterial':
                return 'hw'
        return road_type
    
    delhi_df['road_type'] = delhi_df['road_type'].apply(upgrade_road_type)
    
    # 8. SIGNAL COUNT ADJUSTMENTS (Delhi has more signals)
    print("  🚥 Adjusting signal counts...")
    delhi_df['num_signals'] = delhi_df['num_signals'] + np.random.randint(0, 3, len(delhi_df))
    
    # 9. Add Delhi-specific features
    print("  🌫️ Adding air quality impact...")
    
    def get_visibility_factor(month):
        # Delhi has severe smog in winter (Nov-Feb)
        if month in [11, 12, 1, 2]:
            return np.random.choice(['poor', 'moderate', 'good'], p=[0.4, 0.4, 0.2])
        elif month in [3, 4, 5]:  # Summer dust storms
            return np.random.choice(['poor', 'moderate', 'good'], p=[0.2, 0.5, 0.3])
        else:
            return np.random.choice(['poor', 'moderate', 'good'], p=[0.1, 0.3, 0.6])
    
    delhi_df['visibility'] = delhi_df['month'].apply(get_visibility_factor)
    
    # Round numerical values
    delhi_df['temperature_c'] = delhi_df['temperature_c'].round(1)
    delhi_df['rainfall_mm'] = delhi_df['rainfall_mm'].round(2)
    delhi_df['humidity'] = delhi_df['humidity'].round(1)
    delhi_df['congestion_score'] = delhi_df['congestion_score'].round(2)
    delhi_df['traffic_density'] = delhi_df['traffic_density'].round(2)
    delhi_df['avg_speed'] = delhi_df['avg_speed'].round(2)
    
    return delhi_df


def main():
    print("=" * 70)
    print("Chennai to Delhi Traffic Data Converter")
    print("=" * 70)
    
    # Read Chennai data
    print("\n📂 Reading Chennai synthetic data...")
    chennai_df = pd.read_csv('data/raw/chennai_synthetic2.csv')
    print(f"  ✅ Loaded {len(chennai_df):,} records")
    
    # Convert to Delhi patterns
    delhi_df = convert_to_delhi_patterns(chennai_df)
    
    # Save to new file
    output_file = 'data/raw/delhi_traffic_synthetic.csv'
    delhi_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Delhi traffic data saved: {output_file}")
    print(f"📊 Total records: {len(delhi_df):,}")
    
    # Show comparison
    print("\n" + "=" * 70)
    print("COMPARISON: Chennai vs Delhi")
    print("=" * 70)
    
    comparison = pd.DataFrame({
        'Metric': ['Avg Congestion', 'Avg Speed (km/h)', 'Avg Temperature (°C)', 
                   'Avg Rainfall (mm)', 'Avg Humidity (%)'],
        'Chennai (Original)': [
            chennai_df['congestion_score'].mean(),
            chennai_df['avg_speed'].mean(),
            chennai_df['temperature_c'].mean(),
            chennai_df['rainfall_mm'].mean(),
            chennai_df['humidity'].mean()
        ],
        'Delhi (Adjusted)': [
            delhi_df['congestion_score'].mean(),
            delhi_df['avg_speed'].mean(),
            delhi_df['temperature_c'].mean(),
            delhi_df['rainfall_mm'].mean(),
            delhi_df['humidity'].mean()
        ]
    })
    
    print(comparison.to_string(index=False))
    
    print("\n📈 Delhi-specific characteristics:")
    print(f"  • Road types: {delhi_df['road_type'].value_counts().to_dict()}")
    print(f"  • Visibility distribution: {delhi_df['visibility'].value_counts().to_dict()}")
    print(f"  • Peak hour congestion: {delhi_df[delhi_df['is_peak_hour']==1]['congestion_score'].mean():.2f}")
    print(f"  • Non-peak congestion: {delhi_df[delhi_df['is_peak_hour']==0]['congestion_score'].mean():.2f}")
    
    print("\n" + "=" * 70)
    print("✅ Conversion complete! Data ready for Delhi ML training")
    print("=" * 70)


if __name__ == "__main__":
    main()
