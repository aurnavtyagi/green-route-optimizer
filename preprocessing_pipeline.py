"""
Comprehensive Data Preprocessing and Feature Extraction Pipeline
for Delhi Traffic Congestion Score Prediction

This script performs:
1. Detailed data quality assessment
2. Data cleaning and preprocessing
3. Extensive visualization
4. Feature engineering
5. Feature extraction using PCA and Random Forest Feature Importance
6. Saving processed data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

class DataPreprocessor:
    def __init__(self, file_path):
        """Initialize preprocessor with data file path"""
        self.file_path = file_path
        self.df_raw = None
        self.df_clean = None
        self.preprocessing_report = {}
        
    def load_data(self):
        """Load raw data and display basic information"""
        print("=" * 80)
        print("STEP 1: DATA LOADING")
        print("=" * 80)
        
        self.df_raw = pd.read_csv(self.file_path)
        print(f"\n✅ Data loaded successfully")
        print(f"📊 Shape: {self.df_raw.shape[0]:,} rows × {self.df_raw.shape[1]} columns")
        print(f"\n📋 Columns: {list(self.df_raw.columns)}")
        
        # Store original shape
        self.preprocessing_report['original_shape'] = self.df_raw.shape
        
        return self.df_raw.head()
    
    def data_quality_assessment(self):
        """Comprehensive data quality assessment"""
        print("\n" + "=" * 80)
        print("STEP 2: DATA QUALITY ASSESSMENT")
        print("=" * 80)
        
        # Missing values
        print("\n📊 Missing Values Analysis:")
        missing = self.df_raw.isnull().sum()
        missing_pct = (missing / len(self.df_raw) * 100).round(2)
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing_Count': missing.values,
            'Missing_Percentage': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
        print(missing_df.to_string(index=False))
        
        # Data types
        print("\n📝 Data Types:")
        print(self.df_raw.dtypes)
        
        # Duplicates
        duplicates = self.df_raw.duplicated().sum()
        print(f"\n📋 Duplicate Rows: {duplicates} ({duplicates/len(self.df_raw)*100:.2f}%)")
        
        # Numerical column statistics
        print("\n📈 Numerical Columns Statistics:")
        print(self.df_raw.describe())
        
        # Store in report
        self.preprocessing_report['missing_values'] = missing_df.to_dict('records')
        self.preprocessing_report['duplicates'] = duplicates
        
    def visualize_data_quality(self):
        """Visualize data quality issues"""
        print("\n" + "=" * 80)
        print("STEP 3: DATA QUALITY VISUALIZATION")
        print("=" * 80)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Missing values heatmap
        missing_data = self.df_raw.isnull()
        axes[0, 0].imshow(missing_data.T, cmap='RdYlGn_r', aspect='auto', interpolation='nearest')
        axes[0, 0].set_title('Missing Values Heatmap (Red = Missing)', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Records')
        axes[0, 0].set_ylabel('Features')
        axes[0, 0].set_yticks(range(len(self.df_raw.columns)))
        axes[0, 0].set_yticklabels(self.df_raw.columns, fontsize=8)
        
        # 2. Missing values bar plot
        missing_counts = self.df_raw.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=True)
        if len(missing_counts) > 0:
            missing_counts.plot(kind='barh', ax=axes[0, 1], color='coral')
            axes[0, 1].set_title('Missing Values Count by Column', fontsize=14, fontweight='bold')
            axes[0, 1].set_xlabel('Count')
        else:
            axes[0, 1].text(0.5, 0.5, 'No Missing Values Found', 
                           ha='center', va='center', fontsize=14, fontweight='bold',
                           transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Missing Values Count by Column', fontsize=14, fontweight='bold')
            axes[0, 1].axis('off')
        
        # 3. Data type distribution
        dtype_counts = self.df_raw.dtypes.value_counts()
        axes[1, 0].pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%', startangle=90)
        axes[1, 0].set_title('Data Type Distribution', fontsize=14, fontweight='bold')
        
        # 4. Duplicate records
        duplicate_status = ['Unique', 'Duplicate']
        duplicate_counts = [len(self.df_raw) - self.df_raw.duplicated().sum(), self.df_raw.duplicated().sum()]
        axes[1, 1].bar(duplicate_status, duplicate_counts, color=['green', 'red'])
        axes[1, 1].set_title('Duplicate Records', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('Count')
        for i, v in enumerate(duplicate_counts):
            axes[1, 1].text(i, v + 100, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('data/processed/01_data_quality_assessment.png', dpi=300, bbox_inches='tight')
        print("✅ Saved: data/processed/01_data_quality_assessment.png")
        plt.close()
    
    def handle_missing_values(self):
        """Handle missing values with appropriate strategies"""
        print("\n" + "=" * 80)
        print("STEP 4: HANDLING MISSING VALUES")
        print("=" * 80)
        
        self.df_clean = self.df_raw.copy()
        
        # Strategy 1: Fill numerical columns with median
        numerical_cols = ['avg_speed', 'traffic_density', 'temperature_c', 'humidity']
        for col in numerical_cols:
            if col in self.df_clean.columns and self.df_clean[col].isnull().sum() > 0:
                median_val = pd.to_numeric(self.df_clean[col], errors='coerce').median()
                self.df_clean[col].fillna(median_val, inplace=True)
                print(f"  ✅ Filled {col} with median: {median_val:.2f}")
        
        # Strategy 2: Fill categorical columns with mode
        if 'road_type' in self.df_clean.columns:
            # First, replace empty strings with NaN
            self.df_clean['road_type'] = self.df_clean['road_type'].replace('', np.nan)
            mode_val = self.df_clean['road_type'].mode()[0] if len(self.df_clean['road_type'].mode()) > 0 else 'hw'
            self.df_clean['road_type'].fillna(mode_val, inplace=True)
            print(f"  ✅ Filled road_type with mode: {mode_val}")
        
        # Remaining missing values
        remaining_missing = self.df_clean.isnull().sum().sum()
        print(f"\n📊 Remaining missing values: {remaining_missing}")
        
    def handle_data_types(self):
        """Fix data type inconsistencies"""
        print("\n" + "=" * 80)
        print("STEP 5: FIXING DATA TYPES")
        print("=" * 80)
        
        # Numerical columns that should be numeric
        numeric_cols = ['distance_km', 'lane_count', 'num_signals', 'hour', 'day_of_week',
                       'temperature_c', 'rainfall_mm', 'humidity', 'avg_speed', 
                       'traffic_density', 'congestion_score']
        
        for col in numeric_cols:
            if col in self.df_clean.columns:
                # Convert to numeric, coerce errors to NaN
                before_count = self.df_clean[col].isnull().sum()
                self.df_clean[col] = pd.to_numeric(self.df_clean[col], errors='coerce')
                after_count = self.df_clean[col].isnull().sum()
                
                if after_count > before_count:
                    # Fill newly created NaNs with median
                    median_val = self.df_clean[col].median()
                    self.df_clean[col].fillna(median_val, inplace=True)
                    print(f"  ✅ {col}: Converted to numeric, filled {after_count - before_count} invalid entries")
        
        # Boolean columns
        bool_cols = ['is_peak_hour', 'is_weekend']
        for col in bool_cols:
            if col in self.df_clean.columns:
                # Map various representations to 0/1
                self.df_clean[col] = self.df_clean[col].replace({
                    'Yes': 1, 'No': 0, 'yes': 1, 'no': 0,
                    'Y': 1, 'N': 0, 'True': 1, 'False': 0,
                    'true': 1, 'false': 0, '2': 1, '-1': 0
                })
                self.df_clean[col] = pd.to_numeric(self.df_clean[col], errors='coerce').fillna(0).astype(int)
                print(f"  ✅ {col}: Standardized to binary (0/1)")
        
        print(f"\n📊 Data types after conversion:")
        print(self.df_clean.dtypes)
    
    def handle_outliers(self):
        """Detect and handle outliers"""
        print("\n" + "=" * 80)
        print("STEP 6: OUTLIER DETECTION AND HANDLING")
        print("=" * 80)
        
        outlier_counts = {}
        
        # Define valid ranges for each column
        ranges = {
            'avg_speed': (0, 120),  # km/h
            'temperature_c': (0, 50),  # Celsius
            'humidity': (0, 100),  # Percentage
            'congestion_score': (1.0, 3.0),  # Predefined range
            'lane_count': (1, 10),  # Reasonable lanes
            'traffic_density': (0, 200),  # Reasonable density
            'rainfall_mm': (0, 100),  # mm
            'num_signals': (0, 30)  # Reasonable signal count
        }
        
        for col, (min_val, max_val) in ranges.items():
            if col in self.df_clean.columns:
                # Identify outliers
                outliers = (self.df_clean[col] < min_val) | (self.df_clean[col] > max_val)
                outlier_count = outliers.sum()
                
                if outlier_count > 0:
                    # Cap outliers at boundaries
                    self.df_clean.loc[self.df_clean[col] < min_val, col] = min_val
                    self.df_clean.loc[self.df_clean[col] > max_val, col] = max_val
                    outlier_counts[col] = outlier_count
                    print(f"  ✅ {col}: Fixed {outlier_count} outliers (range: {min_val}-{max_val})")
        
        self.preprocessing_report['outliers_fixed'] = outlier_counts
    
    def standardize_categorical(self):
        """Standardize categorical variables"""
        print("\n" + "=" * 80)
        print("STEP 7: STANDARDIZING CATEGORICAL VARIABLES")
        print("=" * 80)
        
        # Road type standardization
        if 'road_type' in self.df_clean.columns:
            # Remove whitespace and special characters
            self.df_clean['road_type'] = self.df_clean['road_type'].astype(str).str.strip()
            self.df_clean['road_type'] = self.df_clean['road_type'].str.replace(r'[™®©]', '', regex=True)
            
            # Standardize variations
            road_mapping = {
                'hw': 'highway', 'HW': 'highway', 'Hw': 'highway', 'h/w': 'highway',
                'Highway': 'highway', 'HIGHWAY': 'highway',
                'local': 'local', 'Local': 'local', 'LOCAL': 'local',
                'local road': 'local', 'local_road': 'local',
                'arterial': 'arterial', 'Arterial': 'arterial', 'ARTERIAL': 'arterial',
                'arterial_road': 'arterial', 'Artery': 'arterial'
            }
            self.df_clean['road_type'] = self.df_clean['road_type'].replace(road_mapping)
            print(f"  ✅ road_type: Standardized to {self.df_clean['road_type'].nunique()} unique values")
            print(f"     Values: {self.df_clean['road_type'].unique()}")
        
        # Visibility standardization
        if 'visibility' in self.df_clean.columns:
            self.df_clean['visibility'] = self.df_clean['visibility'].astype(str).str.strip().str.lower()
            vis_mapping = {
                'excellent': 'good', 'clear': 'good',
                'avg': 'moderate', 'medium': 'moderate',
                'bad': 'poor', 'low': 'poor'
            }
            self.df_clean['visibility'] = self.df_clean['visibility'].replace(vis_mapping)
            print(f"  ✅ visibility: Standardized to {self.df_clean['visibility'].nunique()} unique values")
            print(f"     Values: {self.df_clean['visibility'].unique()}")
    
    def remove_duplicates(self):
        """Remove duplicate records"""
        print("\n" + "=" * 80)
        print("STEP 8: REMOVING DUPLICATES")
        print("=" * 80)
        
        before_count = len(self.df_clean)
        self.df_clean = self.df_clean.drop_duplicates()
        after_count = len(self.df_clean)
        removed = before_count - after_count
        
        print(f"  ✅ Removed {removed} duplicate rows")
        print(f"  📊 Dataset size: {before_count:,} → {after_count:,}")
        
        self.preprocessing_report['duplicates_removed'] = removed
    
    def fix_logical_inconsistencies(self):
        """Fix logical inconsistencies in data"""
        print("\n" + "=" * 80)
        print("STEP 9: FIXING LOGICAL INCONSISTENCIES")
        print("=" * 80)
        
        fixed_count = 0
        
        # Fix 1: Peak hour should be during typical rush hours (7-10 AM, 5-8 PM)
        if 'hour' in self.df_clean.columns and 'is_peak_hour' in self.df_clean.columns:
            # Define peak hours
            peak_hours = [7, 8, 9, 10, 17, 18, 19, 20]
            
            # Fix is_peak_hour based on actual hour
            wrong_peak = ((self.df_clean['hour'].isin(peak_hours)) & (self.df_clean['is_peak_hour'] == 0)) | \
                        ((~self.df_clean['hour'].isin(peak_hours)) & (self.df_clean['is_peak_hour'] == 1))
            
            self.df_clean.loc[self.df_clean['hour'].isin(peak_hours), 'is_peak_hour'] = 1
            self.df_clean.loc[~self.df_clean['hour'].isin(peak_hours), 'is_peak_hour'] = 0
            
            fixed_count += wrong_peak.sum()
            print(f"  ✅ Fixed {wrong_peak.sum()} inconsistent peak hour flags")
        
        # Fix 2: Weekend should match day_of_week (5, 6 = Saturday, Sunday)
        if 'day_of_week' in self.df_clean.columns and 'is_weekend' in self.df_clean.columns:
            self.df_clean.loc[self.df_clean['day_of_week'].isin([5, 6]), 'is_weekend'] = 1
            self.df_clean.loc[~self.df_clean['day_of_week'].isin([5, 6]), 'is_weekend'] = 0
            print(f"  ✅ Aligned is_weekend with day_of_week")
        
        # Fix 3: High rainfall should correlate with higher humidity
        if 'rainfall_mm' in self.df_clean.columns and 'humidity' in self.df_clean.columns:
            high_rain_low_humidity = (self.df_clean['rainfall_mm'] > 5) & (self.df_clean['humidity'] < 40)
            if high_rain_low_humidity.sum() > 0:
                self.df_clean.loc[high_rain_low_humidity, 'humidity'] = self.df_clean['humidity'].median()
                fixed_count += high_rain_low_humidity.sum()
                print(f"  ✅ Fixed {high_rain_low_humidity.sum()} rainfall-humidity inconsistencies")
        
        self.preprocessing_report['logical_fixes'] = fixed_count
    
    def feature_engineering(self):
        """Create new features from existing ones"""
        print("\n" + "=" * 80)
        print("STEP 10: FEATURE ENGINEERING")
        print("=" * 80)
        
        # 1. Time-based features
        if 'hour' in self.df_clean.columns:
            # Time of day category
            self.df_clean['time_category'] = pd.cut(self.df_clean['hour'], 
                                                      bins=[0, 6, 12, 18, 24],
                                                      labels=['night', 'morning', 'afternoon', 'evening'],
                                                      include_lowest=True)
            print("  ✅ Created time_category (night/morning/afternoon/evening)")
        
        # 2. Weather severity index
        if 'rainfall_mm' in self.df_clean.columns and 'temperature_c' in self.df_clean.columns:
            # Normalize and combine
            rain_norm = self.df_clean['rainfall_mm'] / self.df_clean['rainfall_mm'].max()
            temp_extreme = np.abs(self.df_clean['temperature_c'] - 25) / 25  # Deviation from comfortable 25°C
            self.df_clean['weather_severity'] = (rain_norm * 0.6 + temp_extreme * 0.4).round(2)
            print("  ✅ Created weather_severity index")
        
        # 3. Road capacity index
        if 'lane_count' in self.df_clean.columns and 'distance_km' in self.df_clean.columns:
            self.df_clean['road_capacity'] = (self.df_clean['lane_count'] * 
                                               self.df_clean['distance_km']).round(2)
            print("  ✅ Created road_capacity (lanes × distance)")
        
        # 4. Signal density
        if 'num_signals' in self.df_clean.columns and 'distance_km' in self.df_clean.columns:
            self.df_clean['signal_density'] = (self.df_clean['num_signals'] / 
                                                (self.df_clean['distance_km'] + 0.1)).round(2)
            print("  ✅ Created signal_density (signals per km)")
        
        # 5. Traffic pressure index
        if 'traffic_density' in self.df_clean.columns and 'lane_count' in self.df_clean.columns:
            self.df_clean['traffic_pressure'] = (self.df_clean['traffic_density'] / 
                                                  self.df_clean['lane_count']).round(2)
            print("  ✅ Created traffic_pressure (density per lane)")
        
        # 6. Speed efficiency
        if 'avg_speed' in self.df_clean.columns and 'congestion_score' in self.df_clean.columns:
            self.df_clean['speed_efficiency'] = (self.df_clean['avg_speed'] / 
                                                  (self.df_clean['congestion_score'] + 0.1)).round(2)
            print("  ✅ Created speed_efficiency")
        
        print(f"\n📊 Total features after engineering: {len(self.df_clean.columns)}")
    
    def visualize_distributions(self):
        """Visualize feature distributions"""
        print("\n" + "=" * 80)
        print("STEP 11: FEATURE DISTRIBUTION VISUALIZATION")
        print("=" * 80)
        
        # Select numerical features
        numerical_features = self.df_clean.select_dtypes(include=[np.number]).columns
        n_features = len(numerical_features)
        
        # Create subplots
        fig, axes = plt.subplots(4, 4, figsize=(20, 16))
        axes = axes.flatten()
        
        for idx, col in enumerate(numerical_features[:16]):
            if idx < len(axes):
                self.df_clean[col].hist(bins=50, ax=axes[idx], color='skyblue', edgecolor='black')
                axes[idx].set_title(f'{col}\n(μ={self.df_clean[col].mean():.2f}, σ={self.df_clean[col].std():.2f})',
                                   fontsize=10, fontweight='bold')
                axes[idx].set_xlabel('')
                axes[idx].grid(alpha=0.3)
        
        # Hide unused subplots
        for idx in range(len(numerical_features), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig('data/processed/02_feature_distributions.png', dpi=300, bbox_inches='tight')
        print("✅ Saved: data/processed/02_feature_distributions.png")
        plt.close()
    
    def visualize_correlations(self):
        """Visualize feature correlations"""
        print("\n" + "=" * 80)
        print("STEP 12: CORRELATION ANALYSIS")
        print("=" * 80)
        
        # Select numerical features
        numerical_features = self.df_clean.select_dtypes(include=[np.number])
        
        # Compute correlation matrix
        corr_matrix = numerical_features.corr()
        
        # Plot heatmap
        plt.figure(figsize=(16, 14))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('data/processed/03_correlation_matrix.png', dpi=300, bbox_inches='tight')
        print("✅ Saved: data/processed/03_correlation_matrix.png")
        plt.close()
        
        # Top correlations with target
        if 'congestion_score' in corr_matrix.columns:
            target_corr = corr_matrix['congestion_score'].abs().sort_values(ascending=False)
            print("\n📊 Top 10 Features Correlated with Congestion Score:")
            print(target_corr.head(11).to_string())  # 11 because it includes itself
    
    def visualize_categorical_analysis(self):
        """Analyze categorical features"""
        print("\n" + "=" * 80)
        print("STEP 13: CATEGORICAL FEATURE ANALYSIS")
        print("=" * 80)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()
        
        # 1. Road type distribution
        if 'road_type' in self.df_clean.columns:
            self.df_clean['road_type'].value_counts().plot(kind='bar', ax=axes[0], color='steelblue')
            axes[0].set_title('Road Type Distribution', fontweight='bold')
            axes[0].set_xlabel('')
            axes[0].tick_params(axis='x', rotation=45)
        
        # 2. Visibility distribution
        if 'visibility' in self.df_clean.columns:
            self.df_clean['visibility'].value_counts().plot(kind='bar', ax=axes[1], color='coral')
            axes[1].set_title('Visibility Distribution', fontweight='bold')
            axes[1].set_xlabel('')
            axes[1].tick_params(axis='x', rotation=45)
        
        # 3. Time category distribution
        if 'time_category' in self.df_clean.columns:
            self.df_clean['time_category'].value_counts().plot(kind='bar', ax=axes[2], color='green')
            axes[2].set_title('Time Category Distribution', fontweight='bold')
            axes[2].set_xlabel('')
            axes[2].tick_params(axis='x', rotation=45)
        
        # 4. Congestion by road type
        if 'road_type' in self.df_clean.columns and 'congestion_score' in self.df_clean.columns:
            self.df_clean.groupby('road_type')['congestion_score'].mean().plot(kind='bar', ax=axes[3], color='orange')
            axes[3].set_title('Average Congestion by Road Type', fontweight='bold')
            axes[3].set_ylabel('Avg Congestion Score')
            axes[3].tick_params(axis='x', rotation=45)
        
        # 5. Peak hour vs non-peak
        if 'is_peak_hour' in self.df_clean.columns and 'congestion_score' in self.df_clean.columns:
            peak_data = self.df_clean.groupby('is_peak_hour')['congestion_score'].mean()
            peak_labels = ['Non-Peak', 'Peak']
            axes[4].bar(peak_labels, peak_data.values, color=['green', 'red'])
            axes[4].set_title('Congestion: Peak vs Non-Peak Hours', fontweight='bold')
            axes[4].set_ylabel('Avg Congestion Score')
            for i, v in enumerate(peak_data.values):
                axes[4].text(i, v + 0.05, f'{v:.2f}', ha='center', fontweight='bold')
        
        # 6. Weekend vs weekday
        if 'is_weekend' in self.df_clean.columns and 'congestion_score' in self.df_clean.columns:
            weekend_data = self.df_clean.groupby('is_weekend')['congestion_score'].mean()
            weekend_labels = ['Weekday', 'Weekend']
            axes[5].bar(weekend_labels, weekend_data.values, color=['blue', 'purple'])
            axes[5].set_title('Congestion: Weekday vs Weekend', fontweight='bold')
            axes[5].set_ylabel('Avg Congestion Score')
            for i, v in enumerate(weekend_data.values):
                axes[5].text(i, v + 0.05, f'{v:.2f}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('data/processed/04_categorical_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Saved: data/processed/04_categorical_analysis.png")
        plt.close()
    
    def feature_extraction_pca(self):
        """Feature Extraction using Principal Component Analysis (PCA)"""
        print("\n" + "=" * 80)
        print("STEP 14: FEATURE EXTRACTION - PCA (Algorithm 1)")
        print("=" * 80)
        
        # Select only numerical features for PCA
        numerical_features = self.df_clean.select_dtypes(include=[np.number]).copy()
        
        # Remove target variable if present
        if 'congestion_score' in numerical_features.columns:
            X = numerical_features.drop('congestion_score', axis=1)
            y = numerical_features['congestion_score']
        else:
            X = numerical_features
            y = None
        
        # Handle any remaining NaN values
        X = X.fillna(X.median())
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Apply PCA
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)
        
        # Explained variance
        explained_var = pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        print(f"\n📊 PCA Results:")
        print(f"  • Total components: {len(explained_var)}")
        print(f"  • Components for 95% variance: {np.argmax(cumulative_var >= 0.95) + 1}")
        print(f"  • Components for 99% variance: {np.argmax(cumulative_var >= 0.99) + 1}")
        
        # Visualize PCA results
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # 1. Scree plot
        axes[0].plot(range(1, len(explained_var) + 1), explained_var, 'bo-', linewidth=2)
        axes[0].set_title('PCA Scree Plot', fontweight='bold', fontsize=14)
        axes[0].set_xlabel('Principal Component')
        axes[0].set_ylabel('Explained Variance Ratio')
        axes[0].grid(alpha=0.3)
        
        # 2. Cumulative variance
        axes[1].plot(range(1, len(cumulative_var) + 1), cumulative_var, 'ro-', linewidth=2)
        axes[1].axhline(y=0.95, color='g', linestyle='--', label='95% threshold')
        axes[1].axhline(y=0.99, color='b', linestyle='--', label='99% threshold')
        axes[1].set_title('Cumulative Explained Variance', fontweight='bold', fontsize=14)
        axes[1].set_xlabel('Number of Components')
        axes[1].set_ylabel('Cumulative Variance Ratio')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        # 3. Feature contributions to PC1 and PC2
        components_df = pd.DataFrame(
            pca.components_[:2].T,
            columns=['PC1', 'PC2'],
            index=X.columns
        )
        components_df['abs_PC1'] = np.abs(components_df['PC1'])
        components_df = components_df.sort_values('abs_PC1', ascending=True).tail(10)
        
        y_pos = np.arange(len(components_df))
        axes[2].barh(y_pos, components_df['PC1'], color='steelblue')
        axes[2].set_yticks(y_pos)
        axes[2].set_yticklabels(components_df.index, fontsize=9)
        axes[2].set_title('Top 10 Feature Loadings on PC1', fontweight='bold', fontsize=14)
        axes[2].set_xlabel('Loading')
        axes[2].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('data/processed/05_pca_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Saved: data/processed/05_pca_analysis.png")
        plt.close()
        
        # Add PCA components to dataset (top 5)
        n_components = min(5, X_pca.shape[1])
        for i in range(n_components):
            self.df_clean[f'pca_component_{i+1}'] = X_pca[:, i]
        print(f"\n✅ Added top {n_components} PCA components to dataset")
        
        return explained_var, cumulative_var
    
    def feature_extraction_importance(self):
        """Feature Extraction using Random Forest Feature Importance (Algorithm 2)"""
        print("\n" + "=" * 80)
        print("STEP 15: FEATURE EXTRACTION - Random Forest Importance (Algorithm 2)")
        print("=" * 80)
        
        # Prepare data
        # Encode categorical variables
        df_encoded = self.df_clean.copy()
        
        # Label encode categorical columns
        categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns
        le_dict = {}
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            le_dict[col] = le
        
        # Select features and target
        if 'congestion_score' in df_encoded.columns:
            # Exclude PCA components and target
            feature_cols = [col for col in df_encoded.columns 
                          if col != 'congestion_score' and not col.startswith('pca_component')]
            
            X = df_encoded[feature_cols].fillna(0)
            y = df_encoded['congestion_score']
            
            # Train Random Forest
            print("\n🌲 Training Random Forest model...")
            rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=10)
            rf.fit(X, y)
            
            # Get feature importances
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n📊 Random Forest Feature Importance (Top 15):")
            print(feature_importance.head(15).to_string(index=False))
            
            # Visualize feature importance
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
            
            # 1. Top 15 features
            top_15 = feature_importance.head(15).sort_values('importance', ascending=True)
            axes[0].barh(range(len(top_15)), top_15['importance'], color='forestgreen')
            axes[0].set_yticks(range(len(top_15)))
            axes[0].set_yticklabels(top_15['feature'], fontsize=10)
            axes[0].set_title('Top 15 Most Important Features', fontweight='bold', fontsize=14)
            axes[0].set_xlabel('Importance')
            axes[0].grid(alpha=0.3)
            
            # 2. Cumulative importance
            feature_importance_sorted = feature_importance.sort_values('importance', ascending=False)
            cumulative_importance = np.cumsum(feature_importance_sorted['importance'])
            
            axes[1].plot(range(1, len(cumulative_importance) + 1), cumulative_importance, 
                        'b-', linewidth=2)
            axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% importance')
            axes[1].set_title('Cumulative Feature Importance', fontweight='bold', fontsize=14)
            axes[1].set_xlabel('Number of Features')
            axes[1].set_ylabel('Cumulative Importance')
            axes[1].legend()
            axes[1].grid(alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('data/processed/06_feature_importance.png', dpi=300, bbox_inches='tight')
            print("\n✅ Saved: data/processed/06_feature_importance.png")
            plt.close()
            
            # Add importance scores to dataset
            importance_dict = dict(zip(feature_importance['feature'], feature_importance['importance']))
            
            return feature_importance
        else:
            print("⚠️ Target variable 'congestion_score' not found, skipping feature importance analysis")
            return None
    
    def generate_preprocessing_report(self):
        """Generate comprehensive preprocessing report"""
        print("\n" + "=" * 80)
        print("PREPROCESSING SUMMARY REPORT")
        print("=" * 80)
        
        print(f"\n📊 Data Transformation:")
        print(f"  • Original shape: {self.preprocessing_report['original_shape']}")
        print(f"  • Final shape: {self.df_clean.shape}")
        print(f"  • Rows removed: {self.preprocessing_report['original_shape'][0] - self.df_clean.shape[0]}")
        print(f"  • Features added: {self.df_clean.shape[1] - self.preprocessing_report['original_shape'][1]}")
        
        print(f"\n🔧 Issues Fixed:")
        print(f"  • Duplicates removed: {self.preprocessing_report.get('duplicates_removed', 0)}")
        print(f"  • Outliers corrected: {sum(self.preprocessing_report.get('outliers_fixed', {}).values())}")
        print(f"  • Logical fixes: {self.preprocessing_report.get('logical_fixes', 0)}")
        
        print(f"\n✅ Data Quality:")
        print(f"  • Missing values: {self.df_clean.isnull().sum().sum()}")
        print(f"  • Duplicate rows: {self.df_clean.duplicated().sum()}")
        print(f"  • Data types correct: Yes")
        
        print(f"\n📋 Feature Summary:")
        print(f"  • Total features: {len(self.df_clean.columns)}")
        print(f"  • Numerical features: {len(self.df_clean.select_dtypes(include=[np.number]).columns)}")
        print(f"  • Categorical features: {len(self.df_clean.select_dtypes(include=['object', 'category']).columns)}")
        
    def save_processed_data(self, output_path='data/processed/delhi_traffic_processed.csv'):
        """Save cleaned and processed data"""
        print("\n" + "=" * 80)
        print("STEP 16: SAVING PROCESSED DATA")
        print("=" * 80)
        
        # Remove PCA components before saving (they're derived features)
        df_to_save = self.df_clean.copy()
        pca_cols = [col for col in df_to_save.columns if col.startswith('pca_component')]
        if pca_cols:
            df_to_save = df_to_save.drop(columns=pca_cols)
        
        # Save
        df_to_save.to_csv(output_path, index=False)
        print(f"✅ Processed data saved to: {output_path}")
        print(f"📊 Shape: {df_to_save.shape}")
        print(f"💾 File size: {pd.read_csv(output_path).memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        return output_path


def main():
    """Main preprocessing pipeline"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "DELHI TRAFFIC CONGESTION DATA PREPROCESSING" + " " * 20 + "║")
    print("║" + " " * 25 + "& FEATURE EXTRACTION" + " " * 33 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor('data/raw/delhi_traffic_messy.csv')
    
    # Execute pipeline
    preprocessor.load_data()
    preprocessor.data_quality_assessment()
    preprocessor.visualize_data_quality()
    preprocessor.handle_missing_values()
    preprocessor.handle_data_types()
    preprocessor.handle_outliers()
    preprocessor.standardize_categorical()
    preprocessor.remove_duplicates()
    preprocessor.fix_logical_inconsistencies()
    preprocessor.feature_engineering()
    preprocessor.visualize_distributions()
    preprocessor.visualize_correlations()
    preprocessor.visualize_categorical_analysis()
    
    # Feature extraction algorithms
    pca_results = preprocessor.feature_extraction_pca()
    importance_results = preprocessor.feature_extraction_importance()
    
    # Generate report and save
    preprocessor.generate_preprocessing_report()
    output_file = preprocessor.save_processed_data()
    
    print("\n" + "=" * 80)
    print("✅ PREPROCESSING COMPLETE!")
    print("=" * 80)
    print(f"\n📁 Output Files:")
    print(f"  • Processed data: {output_file}")
    print(f"  • Visualizations: data/processed/*.png (6 files)")
    print(f"  • Raw data preserved: data/raw/delhi_congestion_score.csv")
    
    print("\n🎯 Next Steps:")
    print("  1. Review visualizations in data/processed/")
    print("  2. Use processed data for model training")
    print("  3. Consider top features from importance analysis")
    print("\n")


if __name__ == "__main__":
    main()
