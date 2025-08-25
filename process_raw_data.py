import pandas as pd
import os
import glob

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

# Find raw data directory
raw_data_path = "/Users/umasamba/Documents/Citibike_Data/"
if os.path.exists(raw_data_path):
    # Look for unzipped CSV files
    csv_files = glob.glob(os.path.join(raw_data_path, "**/*.csv"), recursive=True)
    print(f"Found {len(csv_files)} CSV files")
    
    # Look specifically for 2017 files
    files_2017 = [f for f in csv_files if '2017' in os.path.basename(f)]
    print(f"Found {len(files_2017)} files with 2017 in name:")
    for f in files_2017[:10]:  # Show first 10
        print(f"  {os.path.basename(f)}")
    
    if files_2017:
        print("\nProcessing 2017 files...")
        trips_2017 = []
        
        for file_path in files_2017[:5]:  # Process first 5 files
            try:
                print(f"Processing {os.path.basename(file_path)}")
                df = pd.read_csv(file_path, nrows=1000)  # Sample 1000 rows
                df = standardize_columns(df)
                
                if 'start_latitude' in df.columns and 'start_longitude' in df.columns:
                    for _, row in df.iterrows():
                        if pd.notna(row['start_latitude']) and pd.notna(row['start_longitude']):
                            trip = {
                                "start": [row['start_latitude'], row['start_longitude']],
                                "end": [row['end_latitude'], row['end_longitude']] if pd.notna(row['end_latitude']) else [row['start_latitude'], row['start_longitude']],
                                "color": "#27ae60"
                            }
                            trips_2017.append(trip)
                            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        if trips_2017:
            with open('2017_trips.json', 'w') as f:
                import json
                json.dump(trips_2017, f)
            print(f"Created 2017_trips.json with {len(trips_2017)} trips")
        else:
            print("No valid 2017 trips found")
    else:
        print("No 2017 files found in raw data")
else:
    print(f"Raw data path not found: {raw_data_path}")
