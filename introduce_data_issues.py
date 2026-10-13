"""
Introduce realistic data quality issues for preprocessing demonstration
This creates a "messy" dataset to showcase data cleaning techniques
"""

import pandas as pd
import numpy as np

def introduce_data_issues(df):
    """
    Introduce various data quality issues for preprocessing demonstration
    """
    
    print("🔧 Introducing data quality issues...")
    
    # Make a copy
    messy_df = df.copy()
    n = len(messy_df)
    
    # 1. MISSING VALUES (8-12% across different columns)
    print("  ❌ Adding missing values...")
    
    # Random missing in numerical columns
    missing_indices_speed = np.random.choice(n, size=int(n * 0.10), replace=False)
    messy_df.loc[missing_indices_speed, 'avg_speed'] = np.nan
    
    missing_indices_density = np.random.choice(n, size=int(n * 0.08), replace=False)
    messy_df.loc[missing_indices_density, 'traffic_density'] = np.nan
    
    missing_indices_temp = np.random.choice(n, size=int(n * 0.05), replace=False)
    messy_df.loc[missing_indices_temp, 'temperature_c'] = np.nan
    
    missing_indices_humidity = np.random.choice(n, size=int(n * 0.06), replace=False)
    messy_df.loc[missing_indices_humidity, 'humidity'] = np.nan
    
    # Some empty strings instead of NaN
    missing_indices_road = np.random.choice(n, size=int(n * 0.03), replace=False)
    messy_df.loc[missing_indices_road, 'road_type'] = ''
    
    
    # 2. INVALID/OUTLIER VALUES
    print("  ⚠️ Adding invalid entries...")
    
    # Negative speeds (data entry errors)
    negative_indices = np.random.choice(n, size=int(n * 0.02), replace=False)
    messy_df.loc[negative_indices, 'avg_speed'] = -messy_df.loc[negative_indices, 'avg_speed']
    
    # Unrealistic high speeds (>120 km/h in city traffic)
    high_speed_indices = np.random.choice(n, size=int(n * 0.015), replace=False)
    messy_df.loc[high_speed_indices, 'avg_speed'] = np.random.uniform(150, 250, len(high_speed_indices))
    
    # Impossible temperatures
    temp_outliers = np.random.choice(n, size=int(n * 0.01), replace=False)
    messy_df.loc[temp_outliers, 'temperature_c'] = np.random.choice([-5, -10, 60, 75], len(temp_outliers))
    
    # Invalid humidity (>100% or <0%)
    humidity_outliers = np.random.choice(n, size=int(n * 0.02), replace=False)
    messy_df.loc[humidity_outliers, 'humidity'] = np.random.choice([120, 150, -10, -20], len(humidity_outliers))
    
    # Congestion score out of range (should be 1.0-3.0)
    congestion_outliers = np.random.choice(n, size=int(n * 0.015), replace=False)
    messy_df.loc[congestion_outliers, 'congestion_score'] = np.random.uniform(5, 10, len(congestion_outliers))
    
    # Invalid lane count (0 or too many)
    lane_outliers = np.random.choice(n, size=int(n * 0.01), replace=False)
    messy_df.loc[lane_outliers, 'lane_count'] = 0
    
    high_lane_outliers = np.random.choice(n, size=int(n * 0.005), replace=False)
    messy_df.loc[high_lane_outliers, 'lane_count'] = np.random.randint(15, 30, len(high_lane_outliers))
    
    
    # 3. DATA TYPE ISSUES
    print("  🔤 Adding data type inconsistencies...")
    
    # String values in numeric columns
    string_indices = np.random.choice(n, size=int(n * 0.02), replace=False)
    messy_df.loc[string_indices, 'distance_km'] = np.random.choice(['N/A', 'unknown', 'null', '???'], len(string_indices))
    
    # Mixed numeric formats
    mixed_indices = np.random.choice(n, size=int(n * 0.01), replace=False)
    messy_df.loc[mixed_indices, 'num_signals'] = messy_df.loc[mixed_indices, 'num_signals'].astype(str) + '.0'
    
    
    # 4. INCONSISTENT CATEGORICAL VALUES
    print("  📝 Adding categorical inconsistencies...")
    
    # Road type variations (typos, different cases, extra spaces)
    road_variations = {
        'hw': ['HW', 'Hw', 'hw ', ' hw', 'h/w', 'highway'],
        'local': ['Local', 'LOCAL', 'local ', ' local', 'local road', 'local_road'],
        'arterial': ['Arterial', 'ARTERIAL', 'arterial ', ' arterial', 'Artery', 'arterial_road']
    }
    
    variation_indices = np.random.choice(n, size=int(n * 0.08), replace=False)
    for idx in variation_indices:
        current_road = messy_df.loc[idx, 'road_type']
        if current_road in road_variations:
            messy_df.loc[idx, 'road_type'] = np.random.choice(road_variations[current_road])
    
    # Visibility variations
    visibility_variations = {
        'good': ['Good', 'GOOD', 'good ', 'excellent', 'clear'],
        'moderate': ['Moderate', 'MODERATE', 'moderate ', 'avg', 'medium'],
        'poor': ['Poor', 'POOR', 'poor ', 'bad', 'low']
    }
    
    vis_variation_indices = np.random.choice(n, size=int(n * 0.05), replace=False)
    for idx in vis_variation_indices:
        current_vis = messy_df.loc[idx, 'visibility']
        if current_vis in visibility_variations:
            messy_df.loc[idx, 'visibility'] = np.random.choice(visibility_variations[current_vis])
    
    
    # 5. DUPLICATE ROWS
    print("  📋 Adding duplicate entries...")
    
    # Create exact duplicates (3-5%)
    duplicate_indices = np.random.choice(n, size=int(n * 0.04), replace=False)
    duplicates = messy_df.iloc[duplicate_indices].copy()
    messy_df = pd.concat([messy_df, duplicates], ignore_index=True)
    
    
    # 6. LOGICAL INCONSISTENCIES
    print("  🤔 Adding logical inconsistencies...")
    
    # High rainfall but low humidity
    logic_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.02), replace=False)
    messy_df.loc[logic_indices, 'rainfall_mm'] = np.random.uniform(10, 30, len(logic_indices))
    messy_df.loc[logic_indices, 'humidity'] = np.random.uniform(20, 35, len(logic_indices))
    
    # Peak hour flag doesn't match hour
    peak_logic_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.03), replace=False)
    messy_df.loc[peak_logic_indices, 'hour'] = 3  # 3 AM
    messy_df.loc[peak_logic_indices, 'is_peak_hour'] = 1  # Marked as peak (wrong!)
    
    
    # 7. WHITESPACE ISSUES
    print("  🔲 Adding whitespace problems...")
    
    # Leading/trailing spaces in categorical columns
    space_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.04), replace=False)
    for idx in space_indices:
        if isinstance(messy_df.loc[idx, 'road_type'], str):
            messy_df.loc[idx, 'road_type'] = '  ' + messy_df.loc[idx, 'road_type'] + '  '
    
    
    # 8. SPECIAL CHARACTERS AND UNICODE
    print("  🔣 Adding special character issues...")
    
    special_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.01), replace=False)
    messy_df.loc[special_indices, 'road_type'] = np.random.choice(['hw™', 'local®', 'arterial©'], len(special_indices))
    
    
    # 9. INCORRECT BOOLEAN VALUES
    print("  ✓ Adding boolean inconsistencies...")
    
    # is_peak_hour and is_weekend should be 0/1, add other values
    bool_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.02), replace=False)
    messy_df.loc[bool_indices, 'is_peak_hour'] = np.random.choice(['Yes', 'No', 'True', 'False', '2', '-1'], len(bool_indices))
    
    weekend_indices = np.random.choice(len(messy_df), size=int(len(messy_df) * 0.015), replace=False)
    messy_df.loc[weekend_indices, 'is_weekend'] = np.random.choice(['Y', 'N', 'yes', 'no'], len(weekend_indices))
    
    
    return messy_df


def main():
    print("=" * 70)
    print("Data Quality Issues Introducer")
    print("Creating messy dataset for preprocessing demonstration")
    print("=" * 70)
    
    # Read clean data
    print("\n📂 Reading clean Delhi traffic data...")
    clean_df = pd.read_csv('data/raw/delhi_congestion_score.csv')
    print(f"  ✅ Loaded {len(clean_df):,} clean records")
    
    # Introduce issues
    messy_df = introduce_data_issues(clean_df)
    
    # Shuffle to mix issues throughout
    messy_df = messy_df.sample(frac=1).reset_index(drop=True)
    
    # Save messy version
    output_file = 'data/raw/delhi_traffic_messy.csv'
    messy_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Messy dataset saved: {output_file}")
    print(f"📊 Total records: {len(messy_df):,} (includes duplicates)")
    
    # Summary of issues
    print("\n" + "=" * 70)
    print("DATA QUALITY ISSUES SUMMARY")
    print("=" * 70)
    
    issues = {
        'Missing values in avg_speed': messy_df['avg_speed'].isna().sum(),
        'Missing values in traffic_density': messy_df['traffic_density'].isna().sum(),
        'Missing values in temperature': messy_df['temperature_c'].isna().sum(),
        'Missing values in humidity': messy_df['humidity'].isna().sum(),
        'Empty road_type': (messy_df['road_type'] == '').sum(),
        'Duplicate rows': len(messy_df) - len(messy_df.drop_duplicates()),
        'Unique road_type variants': messy_df['road_type'].nunique(),
        'Unique visibility variants': messy_df['visibility'].nunique(),
    }
    
    for issue, count in issues.items():
        print(f"  • {issue}: {count}")
    
    print("\n📝 Issues introduced for preprocessing demonstration:")
    print("  1. ❌ Missing values (NaN, empty strings)")
    print("  2. ⚠️ Invalid/outlier values (negative speeds, extreme temps)")
    print("  3. 🔤 Data type inconsistencies (strings in numeric columns)")
    print("  4. 📝 Categorical inconsistencies (typos, case variations)")
    print("  5. 📋 Duplicate rows")
    print("  6. 🤔 Logical inconsistencies (peak hour at 3 AM)")
    print("  7. 🔲 Whitespace issues (leading/trailing spaces)")
    print("  8. 🔣 Special characters")
    print("  9. ✓ Boolean value variations (Yes/No instead of 0/1)")
    
    print("\n" + "=" * 70)
    print("✅ Messy dataset ready for preprocessing demonstration!")
    print("=" * 70)
    print("\nNext step: Create preprocessing script to clean this data")


if __name__ == "__main__":
    main()
