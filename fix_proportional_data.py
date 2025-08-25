import json

# Based on the actual counts we found:
actual_trips = {
    2013: 22459552,
    2014: 16162432, 
    2015: 19875938,
    2016: 27691310,
    2017: 16364657,
    2018: 70901140,
    2019: 41913288,
    2020: 673604,    # COVID crash
    2021: 1288886,   # Recovery
    2022: 1682468,
    2023: 1977702,
    2024: 95861374   # Massive growth!
}

# Calculate proportional visualization points
# Use 2020 as baseline (smallest) = 100 points
baseline_year = 2020
baseline_trips = actual_trips[2020]
baseline_points = 100

print("Proportional visualization points:")
for year in range(2013, 2025):
    trips = actual_trips[year]
    # Calculate proportional points
    points = int((trips / baseline_trips) * baseline_points)
    print(f"{year}: {trips:,} trips → {points:,} points")

# Load existing files and check if they match this proportion
print("\nCurrent file sizes:")
for year in range(2013, 2025):
    try:
        with open(f'{year}_trips.json', 'r') as f:
            current_data = json.load(f)
            current_count = len(current_data)
            expected_points = int((actual_trips[year] / baseline_trips) * baseline_points)
            print(f"{year}: {current_count} (expected: {expected_points})")
    except:
        print(f"{year}: file not found")
