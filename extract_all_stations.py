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

for year in range(2013, 2025):
    year_files = [f for f in csv_files if str(year) in os.path.basename(f)]
    
    if year_files:
        print(f"Processing ALL data for {year}...")
        unique_stations = set()
        trip_count = 0
        
        for file_path in year_files:
            try:
                # Process in chunks to handle large files
                for chunk in pd.read_csv(file_path, chunksize=10000):
                    chunk = standardize_columns(chunk)
                    
                    if 'start_latitude' in chunk.columns and 'start_longitude' in chunk.columns:
                        for _, row in chunk.iterrows():
                            trip_count += 1
                            if pd.notna(row['start_latitude']) and pd.notna(row['start_longitude']):
                                # Round coordinates to create unique stations
                                lat = round(row['start_latitude'], 4)
                                lng = round(row['start_longitude'], 4)
                                unique_stations.add((lat, lng))
                                
            except Exception as e:
                print(f"  Error with {os.path.basename(file_path)}: {e}")
                continue
        
        # Convert to trip format
        trips = []
        for lat, lng in unique_stations:
            trip = {
                "start": [lat, lng],
                "end": [lat, lng],
                "color": "#3498db"
            }
            trips.append(trip)
        
        filename = f"{year}_trips.json"
        with open(filename, 'w') as f:
            json.dump(trips, f)
        
        print(f"  {year}: {trip_count:,} total trips → {len(trips)} unique stations")
    else:
        print(f"No files found for {year}")

print("\nCompleted processing all actual data!")
