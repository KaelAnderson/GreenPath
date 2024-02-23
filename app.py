import streamlit as st
import googlemaps
import polyline
import pandas as pd

# Set up Google Maps API client
gmaps = googlemaps.Client(key='AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo')  # Replace 'YOUR_API_KEY' with your actual API key

# Function to load Vehicle Database
@st.cache_data
def load_data():
    df = pd.read_csv('VEHICLES5.csv')
    return df

# Streamlit app layout
st.title('Display Route on Google Maps')

# Create two columns layout
col1, col2 = st.columns([2, 1])

# Input for start and end locations
with col1:
    start_loc = st.text_input("Enter starting location (e.g., 'New York'):")
    end_loc = st.text_input("Enter destination location (e.g., 'Los Angeles'):")

# Button to generate route
with col1:
    if st.button("Show Route"):
        # Get directions from Google Maps API
        directions = gmaps.directions(start_loc, end_loc)

        # Extract polyline from directions
        if directions:
            steps = directions[0]['legs'][0]['steps']
            polyline_points = []
            for step in steps:
                polyline_points.extend(polyline.decode(step['polyline']['points']))

            # Extract latitudes and longitudes from polyline points
            lats = [point[0] for point in polyline_points]
            lons = [point[1] for point in polyline_points]

            # Display map with route
            st.map({'lat': lats, 'lon': lons,}, color='#75cf70')
        else:
            st.error("No route found. Please check your locations.")
            
# You can use col2 for additional content, such as info or settings if needed
with col2:
    # Load the data
    df = load_data()

    # Unique makes
    makes = df['make'].unique()

    # Dropdown for selecting make
    selected_make = st.selectbox("Select Make:", makes)

    # Filter data based on selected make
    filtered_data = df[df['make'] == selected_make]

    # Unique models for the selected make
    models = filtered_data['model'].unique()

    # Dropdown for selecting model
    selected_model = st.selectbox("Select Model:", models)

    st.write("You have selected:")
    selected_data = filtered_data[filtered_data['model'] == selected_model]
    st.write(selected_data)
