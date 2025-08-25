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

# Correct proportional targets
targets = {
    2013: 3334, 2014: 2399, 2015: 2950, 2016: 4110, 2017: 2429,
    2018: 10525, 2019: 6222, 2020: 100, 2021: 191, 2022: 249, 2023: 293, 2024: 14231
}

raw_data_path = "/Users/umasamba/Documents/Citibike_Data/"
csv_files = glob.glob(os.path.join(raw_data_path, "**/*.csv"), recursive=True)

for year in range(2013, 2025):
    year_files = [f for f in csv_files if str(year) in os.path.basename(f)]
    target = targets[year]
    
    if year_files:
        print(f"Creating {year}: target {target} trips")
        trips = []
        
        # Calculate trips per file to reach target
        trips_per_file = max(1, target // len(year_files))
        
        for file_path in year_files:
            if len(trips) >= target:
                break
                
            try:
                needed = min(trips_per_file, target - len(trips))
                df = pd.read_csv(file_path, nrows=needed * 2)  # Read extra in case of invalid data
                df = standardize_columns(df)
                
                if 'start_latitude' in df.columns and 'start_longitude' in df.columns:
                    for _, row in df.iterrows():
                        if len(trips) >= target:
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
        print(f"  Created {filename} with {len(trips)} trips")
    else:
        print(f"No files found for {year}")

print("Completed creating correctly proportioned data!")
