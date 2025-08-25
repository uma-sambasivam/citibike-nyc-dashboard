import json
import os
import glob
import pandas as pd

# Look for any files that might contain 2017 data
csv_path = "/Users/umasamba/Documents/Citibike_Data/Processed_Clean/"
csv_files = glob.glob(os.path.join(csv_path, "*.csv"))

trips_2017 = []

print("Searching for 2017 data...")
for i, csv_file in enumerate(csv_files):
    filename = os.path.basename(csv_file)
    
    # Check files that might contain 2017 data
    if any(x in filename for x in ['2017', '201701', '201702', '201703', '201704', '201705', '201706', 
                                   '201707', '201708', '201709', '201710', '201711', '201712']):
        print(f"Found potential 2017 file: {filename}")
        
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            df['start_time'] = pd.to_datetime(df['start_time'])
            df_2017 = df[df['start_time'].dt.year == 2017]
            
            if len(df_2017) > 0:
                print(f"  -> Found {len(df_2017)} trips from 2017")
                
                # Sample some trips
                sample_size = min(200, len(df_2017))
                df_sample = df_2017.sample(n=sample_size)
                
                for _, row in df_sample.iterrows():
                    trip = {
                        "start": [row['start_latitude'], row['start_longitude']],
                        "end": [row['end_latitude'], row['end_longitude']],
                        "color": "#1abc9c"
                    }
                    trips_2017.append(trip)
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Also check some files around 2017 timeframe
print("\nChecking files around 2017 timeframe...")
for csv_file in csv_files[:50]:  # Check first 50 files
    try:
        df = pd.read_csv(csv_file, low_memory=False, nrows=100)  # Just check first 100 rows
        df['start_time'] = pd.to_datetime(df['start_time'])
        
        if any(df['start_time'].dt.year == 2017):
            filename = os.path.basename(csv_file)
            print(f"Found 2017 data in: {filename}")
            
            # Process full file
            df_full = pd.read_csv(csv_file, low_memory=False)
            df_full['start_time'] = pd.to_datetime(df_full['start_time'])
            df_2017 = df_full[df_full['start_time'].dt.year == 2017]
            
            sample_size = min(200, len(df_2017))
            df_sample = df_2017.sample(n=sample_size)
            
            for _, row in df_sample.iterrows():
                trip = {
                    "start": [row['start_latitude'], row['start_longitude']],
                    "end": [row['end_latitude'], row['end_longitude']],
                    "color": "#1abc9c"
                }
                trips_2017.append(trip)
                
    except:
        continue

print(f"\nTotal 2017 trips found: {len(trips_2017)}")

if trips_2017:
    with open('2017_trips.json', 'w') as f:
        json.dump(trips_2017, f)
    print("Created 2017_trips.json")
else:
    print("No 2017 trips found")
