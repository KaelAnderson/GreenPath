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
st.title('GreenPath')
            
col1, col2, col3 = st.columns(3)

# Load the data
df = load_data()

# Unique makes
makes = df['make'].unique()

with col1:
    # Dropdown for selecting make
    selected_make = st.selectbox("Select Make:", makes)

# Filter data based on selected make
filtered_data = df[df['make'] == selected_make]

# Unique models for the selected make
models = filtered_data['model'].unique()

with col2:
    # Dropdown for selecting model
    selected_model = st.selectbox("Select Model:", models)

filtered_data = filtered_data[filtered_data['model'] == selected_model]

# Unique years for the selected make and model
years = filtered_data['year'].unique()

with col3:
    selected_year = st.selectbox("Select Year:", years)

filtered_data = filtered_data[filtered_data['year'] == selected_year]

#gets the value of the selected make model and year
if not filtered_data.empty:
    comb08_value = filtered_data['comb08'].values[0]
else:
    st.write("No data available for the selected make, model, and year.")

col4, col5 = st.columns(2)

with col4:
    isCarpool = st.selectbox('How are you riding?', ('Solo', 'Carpool'))

with col5:
    numPeople = st.number_input("How many people are in the car?", value=1, min_value=1)
    # might want to put a max value on that. definitely would want to based on make and model but that's not really smth we can do rn


# Input for start and end locations
start_loc = st.text_input("Enter starting location (e.g., 'New York'):")
end_loc = st.text_input("Enter destination location (e.g., 'Los Angeles'):")

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
