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
        'member_casual': 'user_type',
        'Trip Duration': 'trip_duration',
        'Start Time': 'start_time',
        'Stop Time': 'end_time',
        'Start Station ID': 'start_station_id',
        'Start Station Name': 'start_station_name',
        'Start Station Latitude': 'start_latitude',
        'Start Station Longitude': 'start_longitude',
        'End Station ID': 'end_station_id',
        'End Station Name': 'end_station_name',
        'End Station Latitude': 'end_latitude',
        'End Station Longitude': 'end_longitude',
        'Bike ID': 'bike_id',
        'User Type': 'user_type',
        'Birth Year': 'birth_year',
        'Gender': 'gender'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    return df

# Find all CSV files
raw_data_path = "/Users/umasamba/Documents/Citibike_Data/"
csv_files = glob.glob(os.path.join(raw_data_path, "**/*.csv"), recursive=True)

# Group files by year
yearly_files = {}
for year in range(2013, 2025):
    yearly_files[year] = [f for f in csv_files if str(year) in os.path.basename(f)]

# Check what we have
print("Year-by-year file count:")
for year in range(2013, 2025):
    count = len(yearly_files[year])
    print(f"{year}: {count} files")

# Process each year to create trip files
for year in range(2013, 2025):
    if yearly_files[year]:
        print(f"\nProcessing {year}...")
        trips = []
        
        # Process up to 3 files per year to keep manageable
        for file_path in yearly_files[year][:3]:
            try:
                df = pd.read_csv(file_path, nrows=500)  # 500 trips per file
                df = standardize_columns(df)
                
                if 'start_latitude' in df.columns and 'start_longitude' in df.columns:
                    for _, row in df.iterrows():
                        if pd.notna(row['start_latitude']) and pd.notna(row['start_longitude']):
                            trip = {
                                "start": [row['start_latitude'], row['start_longitude']],
                                "end": [row['end_latitude'], row['end_longitude']] if pd.notna(row['end_latitude']) else [row['start_latitude'], row['start_longitude']],
                                "color": "#3498db"
                            }
                            trips.append(trip)
                            
            except Exception as e:
                print(f"  Error with {os.path.basename(file_path)}: {e}")
        
        if trips:
            filename = f"{year}_trips.json"
            with open(filename, 'w') as f:
                json.dump(trips, f)
            print(f"  Created {filename} with {len(trips)} trips")
        else:
            print(f"  No valid trips found for {year}")
    else:
        print(f"\nNo files found for {year}")

print("\nCompleted processing all years!")
