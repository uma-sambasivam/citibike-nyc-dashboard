import pandas as pd
import os
import glob
import json

def standardize_columns(df):
    column_mapping = {
        'tripduration': 'trip_duration',
        'starttime': 'start_time',
        'stoptime': 'end_time',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_latitude',
        'start station longitude': 'start_longitude',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_latitude',
        'end station longitude': 'end_longitude',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
        'birth year': 'birth_year',
        'ride_id': 'trip_id',
        'rideable_type': 'bike_type',
        'started_at': 'start_time',
        'ended_at': 'end_time',
        'start_lat': 'start_latitude',
        'start_lng': 'start_longitude',
        'end_lat': 'end_latitude',
        'end_lng': 'end_longitude',
        'member_casual': 'user_type'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    return df

raw_data_path = "/Users/umasamba/Documents/Citibike_Data/"
csv_files = glob.glob(os.path.join(raw_data_path, "**/*.csv"), recursive=True)

# Count actual trips per year first
print("Counting actual trips per year...")
yearly_counts = {}

for year in range(2013, 2025):
    year_files = [f for f in csv_files if str(year) in os.path.basename(f)]
    total_trips = 0
    
    for file_path in year_files:
        try:
            # Count rows in each file
            df = pd.read_csv(file_path, usecols=[0])  # Just read first column to count
            total_trips += len(df)
        except:
            continue
    
    yearly_counts[year] = total_trips
    print(f"{year}: {total_trips:,} total trips")

# Now extract sample trips proportional to actual data
print("\nExtracting sample trips...")
max_sample = 3000  # Maximum sample size for visualization

for year in range(2013, 2025):
    year_files = [f for f in csv_files if str(year) in os.path.basename(f)]
    total_trips = yearly_counts[year]
    
    if total_trips > 0:
        # Calculate sample size (proportional but capped)
        sample_size = min(max_sample, max(100, total_trips // 1000))
        
        print(f"Processing {year}: {total_trips:,} trips → sampling {sample_size}")
        trips = []
        
        # Distribute sampling across files
        trips_per_file = max(1, sample_size // len(year_files)) if year_files else 0
        
        for file_path in year_files:
            if len(trips) >= sample_size:
                break
                
            try:
                df = pd.read_csv(file_path, nrows=trips_per_file)
                df = standardize_columns(df)
                
                if 'start_latitude' in df.columns and 'start_longitude' in df.columns:
                    for _, row in df.iterrows():
                        if len(trips) >= sample_size:
                            break
                        if pd.notna(row['start_latitude']) and pd.notna(row['start_longitude']):
                            trip = {
                                "start": [row['start_latitude'], row['start_longitude']],
                                "end": [row['end_latitude'], row['end_longitude']] if pd.notna(row['end_latitude']) else [row['start_latitude'], row['start_longitude']],
                                "color": "#3498db"
                            }
                            trips.append(trip)
                            
            except Exception as e:
                continue
        
        filename = f"{year}_trips.json"
        with open(filename, 'w') as f:
            json.dump(trips, f)
        print(f"  Created {filename} with {len(trips)} sample trips")
    else:
        print(f"No data found for {year}")

print("\nCompleted extracting actual proportional data!")
