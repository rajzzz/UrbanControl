import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
import pandas as pd

st.set_page_config(layout="wide")

st.title("🌿 UrbanInfraAI — Green Space Access (Mock Demo)")

# Load mock GeoJSON data
wards = gpd.read_file("data/mock_wards.geojson")
parks = gpd.read_file("data/mock_parks.geojson")
proposed = gpd.read_file("data/mock_proposed_parks.geojson")

# Sidebar filters
st.sidebar.markdown("### 🔍 Search Functionality")

# Search by ward name
ward_names = wards['ward_name'].tolist()
selected_ward = st.sidebar.selectbox("Search by Ward Name:", ["None"] + ward_names)

# Search by coordinates
st.sidebar.markdown("**Or Search by Coordinates:**")
col1, col2 = st.sidebar.columns(2)
with col1:
    search_lat = st.number_input("Latitude:", value=28.6139, format="%.6f", key="search_lat")
with col2:
    search_lon = st.number_input("Longitude:", value=77.2090, format="%.6f", key="search_lon")

search_coords = st.sidebar.button("🔍 Search Coordinates")

# Display search results
def search_area_info(lat, lon, wards_gdf, proposed_gdf):
    """Search for area information by coordinates"""
    search_point = Point(lon, lat)
    
    # Find which ward contains this point
    ward_info = None
    for idx, ward in wards_gdf.iterrows():
        if ward.geometry.contains(search_point):
            ward_info = ward
            break
    
    # Check for nearby proposed parks (within 500m)
    nearby_proposed = []
    for idx, prop in proposed_gdf.iterrows():
        distance = search_point.distance(prop.geometry) * 111000  # rough conversion to meters
        if distance <= 500:  # within 500 meters
            nearby_proposed.append((prop['score'], distance))
    
    return ward_info, nearby_proposed

# Handle search results
search_result = None
if selected_ward != "None":
    ward_data = wards[wards['ward_name'] == selected_ward].iloc[0]
    st.sidebar.markdown(f"### 📍 {selected_ward} Information")
    green_status = "🔴 RED (Underserved)" if ward_data['green_per_person'] < 10 else "🟢 GREEN (Well-served)"
    st.sidebar.markdown(f"**Status:** {green_status}")
    st.sidebar.markdown(f"**Population:** {ward_data['population']:,}")
    st.sidebar.markdown(f"**Green Space per Person:** {ward_data['green_per_person']:.2f} sqm")
    st.sidebar.markdown(f"**Total Green Area:** {ward_data['green_area_sqm']:,} sqm")
    
    # Check for proposed parks in this ward
    ward_geom = wards[wards['ward_name'] == selected_ward].geometry.iloc[0]
    proposed_in_ward = []
    for idx, prop in proposed.iterrows():
        if ward_geom.contains(prop.geometry):
            proposed_in_ward.append(prop['score'])
    
    if proposed_in_ward:
        st.sidebar.markdown(f"**🌳 Proposed Parks:** {len(proposed_in_ward)} park(s)")
        for i, score in enumerate(proposed_in_ward, 1):
            st.sidebar.markdown(f"  - Park {i}: Score {score:.2f}")
    else:
        st.sidebar.markdown("**🌳 Proposed Parks:** None in this ward")

elif search_coords:
    ward_info, nearby_proposed = search_area_info(search_lat, search_lon, wards, proposed)
    
    st.sidebar.markdown(f"### 📍 Location ({search_lat:.4f}, {search_lon:.4f})")
    
    if ward_info is not None:
        green_status = "🔴 RED (Underserved)" if ward_info['green_per_person'] < 10 else "🟢 GREEN (Well-served)"
        st.sidebar.markdown(f"**Ward:** {ward_info['ward_name']}")
        st.sidebar.markdown(f"**Status:** {green_status}")
        st.sidebar.markdown(f"**Population:** {ward_info['population']:,}")
        st.sidebar.markdown(f"**Green Space per Person:** {ward_info['green_per_person']:.2f} sqm")
        
        if nearby_proposed:
            st.sidebar.markdown(f"**🌳 Nearby Proposed Parks:** {len(nearby_proposed)}")
            for i, (score, distance) in enumerate(nearby_proposed, 1):
                st.sidebar.markdown(f"  - Park {i}: Score {score:.2f} ({distance:.0f}m away)")
        else:
            st.sidebar.markdown("**🌳 Nearby Proposed Parks:** None within 500m")
    else:
        st.sidebar.markdown("**Status:** 🟦 Outside mapped wards")
        st.sidebar.markdown("No ward data available for this location")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Display Options")
show_underserved = st.sidebar.checkbox("Show Underserved Wards (<10 sqm/person)", value=True)
show_parks = st.sidebar.checkbox("Show Existing Parks", value=True)
show_proposed = st.sidebar.checkbox("Show Proposed Sites", value=True)

# Base map
# Set map center based on search
map_center = [28.6139, 77.2090]  # Default Delhi center
zoom_level = 12

if selected_ward != "None":
    # Center on selected ward
    ward_geom = wards[wards['ward_name'] == selected_ward].geometry.iloc[0]
    centroid = ward_geom.centroid
    map_center = [centroid.y, centroid.x]
    zoom_level = 14
elif search_coords:
    # Center on searched coordinates
    map_center = [search_lat, search_lon]
    zoom_level = 14

m = folium.Map(
    location=map_center,
    zoom_start=zoom_level,
    tiles='https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite'
)

# Add ESRI labels overlay
folium.TileLayer(
    tiles='https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    attr='Esri Labels',
    name='Labels',
    overlay=True,
    control=True
).add_to(m)

m.save("delhi_satellite_with_labels.html")

# Wards Layer
if show_underserved:
    for _, row in wards.iterrows():
        color = "red" if row["green_per_person"] < 10 else "gray"
        tooltip = (f"Ward: {row['ward_name']}<br>"
                   f"Population: {row['population']}<br>"
                   f"Green/person: {row['green_per_person']:.2f} sqm")
        folium.GeoJson(
            row["geometry"],
            style_function=lambda x, color=color: {
                "fillColor": color, "color": "black", "weight": 1, "fillOpacity": 0.4
            },
            tooltip=tooltip
        ).add_to(m)

# Parks Layer
if show_parks:
    folium.GeoJson(
        parks.geometry,
        name="Existing Parks",
        style_function=lambda x: {
            "fillColor": "green", "color": "green", "weight": 0.5, "fillOpacity": 0.6
        }
    ).add_to(m)

# Proposed Parks
if show_proposed:
    for _, row in proposed.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Proposed Park<br>Score: {row['score']}",
            icon=folium.Icon(color="green", icon="tree-conifer", prefix="glyphicon")
        ).add_to(m)

# Add search location marker
if selected_ward != "None":
    # Get ward centroid for highlighting
    ward_geom = wards[wards['ward_name'] == selected_ward].geometry.iloc[0]
    centroid = ward_geom.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"📍 Searched Ward: {selected_ward}",
        icon=folium.Icon(color="blue", icon="search", prefix="glyphicon")
    ).add_to(m)
    
    # Highlight the selected ward
    ward_data = wards[wards['ward_name'] == selected_ward].iloc[0]
    color = "red" if ward_data["green_per_person"] < 10 else "gray"
    folium.GeoJson(
        ward_geom,
        style_function=lambda x: {
            "fillColor": "yellow", "color": "blue", "weight": 3, "fillOpacity": 0.3
        },
        tooltip=f"🔍 SEARCHED: {selected_ward}"
    ).add_to(m)

elif search_coords:
    # Add marker for searched coordinates
    folium.Marker(
        location=[search_lat, search_lon],
        popup=f"📍 Searched Location<br>({search_lat:.4f}, {search_lon:.4f})",
        icon=folium.Icon(color="blue", icon="search", prefix="glyphicon")
    ).add_to(m)

# Display map
st_data = st_folium(m, width=1200, height=700)

# Add legend below the map
st.markdown("### 🗺️ Map Legend")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("🔴 **Red Areas**: Underserved (<10 sqm/person)")
with col2:
    st.markdown("🟢 **Green Areas**: Existing Parks")
with col3:
    st.markdown("🌳 **Green Pins**: Proposed Park Sites")
with col4:
    st.markdown("🔍 **Blue Pin**: Search Result")

# Summary Statistics
st.markdown("### 📊 Area Summary")
total_population = wards['population'].sum()
underserved_wards = wards[wards['green_per_person'] < 10]
underserved_population = underserved_wards['population'].sum()
underserved_percentage = (underserved_population / total_population) * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Wards", len(wards))
with col2:
    st.metric("Underserved Wards", len(underserved_wards))
with col3:
    st.metric("Underserved Population", f"{underserved_population:,}")
with col4:
    st.metric("% Population Underserved", f"{underserved_percentage:.1f}%")

# Ward details table
st.markdown("### 📋 Ward Details")
ward_summary = wards[['ward_name', 'population', 'green_per_person', 'green_area_sqm']].copy()
ward_summary['status'] = ward_summary['green_per_person'].apply(
    lambda x: "🔴 Underserved" if x < 10 else "🟢 Well-served"
)
ward_summary['green_per_person'] = ward_summary['green_per_person'].round(2)
ward_summary.columns = ['Ward Name', 'Population', 'Green Space (sqm/person)', 'Total Green Area (sqm)', 'Status']
st.dataframe(ward_summary, use_container_width=True)

# Sidebar Justification
st.sidebar.markdown("### EquityAgent Notes")
st.sidebar.write("Wards A and C flagged as underserved with <10 sqm/person.")
st.sidebar.write("Population density and low-income tags used for priority.")

st.sidebar.markdown("### SustainabilityAgent Notes")
st.sidebar.write("Proposed sites avoid water bodies, maximize tree cover potential.")
