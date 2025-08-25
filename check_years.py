import pandas as pd
import glob
import os

csv_path = "/Users/umasamba/Documents/Citibike_Data/Processed_Clean/"
csv_files = glob.glob(os.path.join(csv_path, "*.csv"))

years_found = set()

print("Checking years in data files...")
for i, csv_file in enumerate(csv_files[:20]):  # Check first 20 files
    try:
        df = pd.read_csv(csv_file, low_memory=False, nrows=1000)
        df['start_time'] = pd.to_datetime(df['start_time'])
        file_years = set(df['start_time'].dt.year.unique())
        years_found.update(file_years)
        
        filename = os.path.basename(csv_file)
        print(f"{filename}: {sorted(file_years)}")
        
    except Exception as e:
        print(f"Error with {csv_file}: {e}")

print(f"\nAll years found: {sorted(years_found)}")
