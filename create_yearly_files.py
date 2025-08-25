import json
import os
import glob
import pandas as pd
from datetime import datetime

# Process original CSV files to extract trips by year
csv_path = "/Users/umasamba/Documents/Citibike_Data/Processed_Clean/"
csv_files = glob.glob(os.path.join(csv_path, "*.csv"))
print(f"Found {len(csv_files)} CSV files")

yearly_trips = {year: [] for year in range(2013, 2025)}

# Process each CSV file
for i, csv_file in enumerate(csv_files):
    if i % 50 == 0:
        print(f"Processing file {i+1}/{len(csv_files)}: {os.path.basename(csv_file)}")
    
    try:
        df = pd.read_csv(csv_file, low_memory=False)
        
        # Convert start_time to datetime
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['year'] = df['start_time'].dt.year
        
        # Sample trips from this file (to keep file sizes manageable)
        sample_size = min(100, len(df))
        df_sample = df.sample(n=sample_size) if len(df) > sample_size else df
        
        # Group by year and add to yearly collections
        for year, group in df_sample.groupby('year'):
            if 2013 <= year <= 2024:
                for _, row in group.iterrows():
                    trip = {
                        "start": [row['start_latitude'], row['start_longitude']],
                        "end": [row['end_latitude'], row['end_longitude']],
                        "color": "#3498db"  # Will be overridden by year color
                    }
                    yearly_trips[year].append(trip)
                    
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")
        continue

# Save each year's trips to separate files
for year, trips in yearly_trips.items():
    if trips:  # Only save if we have trips for this year
        filename = f"{year}_trips.json"
        with open(filename, 'w') as f:
            json.dump(trips, f)
        print(f"Created {filename} with {len(trips)} trips")
    else:
        print(f"No trips found for {year}")

print("Yearly trip files created successfully!")
