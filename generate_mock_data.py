import geopandas as gpd
from shapely.geometry import Polygon, Point

# --------------------------
# 1. Mock Ward Boundaries
# --------------------------
wards = gpd.GeoDataFrame({
    "ward_name": ["Ward A", "Ward B", "Ward C"],
    "population": [25000, 18000, 30000],
    "green_area_sqm": [120000, 220000, 200000],
}, geometry=[
    Polygon([(77.1, 28.5), (77.1, 28.52), (77.12, 28.52), (77.12, 28.5)]),
    Polygon([(77.13, 28.5), (77.13, 28.52), (77.15, 28.52), (77.15, 28.5)]),
    Polygon([(77.16, 28.5), (77.16, 28.52), (77.18, 28.52), (77.18, 28.5)])
])

wards["green_per_person"] = wards["green_area_sqm"] / wards["population"]
wards.to_file("data/mock_wards.geojson", driver="GeoJSON")


# --------------------------
# 2. Mock Existing Parks
# --------------------------
parks = gpd.GeoDataFrame({
    "name": ["Park A", "Park B"],
}, geometry=[
    Polygon([(77.105, 28.505), (77.105, 28.51), (77.11, 28.51), (77.11, 28.505)]),
    Polygon([(77.135, 28.505), (77.135, 28.51), (77.14, 28.51), (77.14, 28.505)])
])

parks.to_file("data/mock_parks.geojson", driver="GeoJSON")


# --------------------------
# 3. Mock Proposed Parks
# --------------------------
proposed = gpd.GeoDataFrame({
    "score": [0.85, 0.92],
}, geometry=[
    Point(77.115, 28.506),
    Point(77.165, 28.508)
])

proposed.to_file("data/mock_proposed_parks.geojson", driver="GeoJSON")

print("✅ Mock GeoJSON files created successfully!")
