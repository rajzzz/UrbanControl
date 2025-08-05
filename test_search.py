#!/usr/bin/env python3
"""
Simple test to verify the search functionality works
"""
import geopandas as gpd
from shapely.geometry import Point

# Load mock data
wards = gpd.read_file("data/mock_wards.geojson")
proposed = gpd.read_file("data/mock_proposed_parks.geojson")

print("🧪 Testing Search Functionality")
print("=" * 40)

# Test 1: Ward search
print("\n📍 Test 1: Ward Names Available")
print("Available wards:", wards['ward_name'].tolist())

# Test 2: Coordinate search
print("\n📍 Test 2: Coordinate Search")
test_coords = [
    (28.506, 77.115),  # Should be in Ward A (underserved)
    (28.508, 77.14),   # Should be in Ward B (well-served)
    (28.506, 77.17),   # Should be in Ward C (underserved)
]

for lat, lon in test_coords:
    search_point = Point(lon, lat)
    
    # Find ward
    ward_found = None
    for idx, ward in wards.iterrows():
        if ward.geometry.contains(search_point):
            ward_found = ward
            break
    
    if ward_found is not None:
        status = "🔴 RED (Underserved)" if ward_found['green_per_person'] < 10 else "🟢 GREEN (Well-served)"
        print(f"Coordinates ({lat}, {lon}): {ward_found['ward_name']} - {status}")
        print(f"  Green space: {ward_found['green_per_person']:.2f} sqm/person")
    else:
        print(f"Coordinates ({lat}, {lon}): Outside mapped areas")

# Test 3: Proposed parks
print(f"\n📍 Test 3: Proposed Parks")
print(f"Total proposed parks: {len(proposed)}")
for idx, park in proposed.iterrows():
    print(f"  Park {idx+1}: Score {park['score']:.2f} at ({park.geometry.y:.3f}, {park.geometry.x:.3f})")

print("\n✅ Search functionality test completed!")
