import streamlit as st
import requests
import polyline
import json
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv('VEHICLES5.csv')
    return df

# Function to make the Google Maps API request
def get_eco_friendly_route(start, end, emission_type):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    api_key = "AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo"
    # params = {
    #     "origin": start,
    #     "destination": end,
    #     "emissionType": emission_type,
    #     "requestedReferenceRoutes": ["FUEL_EFFICIENT"],
    #     "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
    #     "key": "AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo"
    # }
    payload = {
        "origin": {"address": start},
        "destination": {"address": end},
        "routeModifiers": {
            "vehicleInfo": {
                "emissionType": "GASOLINE"
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "extraComputations": ["FUEL_CONSUMPTION"],
        "requestedReferenceRoutes": ["FUEL_EFFICIENT"]
    }
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.distanceMeters,routes.duration,routes.routeLabels,routes.polyline,routes.travelAdvisory.fuelConsumptionMicroliters'
    }
    # response = requests.post(url, params=params)
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print(f"data:{data}")
    return data

# Function to decode polyline string into list of coordinates
def decode_polyline(polyline_str):
    return polyline.decode(polyline_str)

# Streamlit app
def main():
    st.title("Greenpath")

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
start = st.text_input("Enter starting point:")
end = st.text_input("Enter destination point:")
emission_type = st.selectbox(
    "Select vehicle emission type:",
    ["DIESEL", "GASOLINE", "ELECTRIC", "HYBRID"],
)

if st.button("Get Eco-Friendly Route"):
    if start and end:
        try:
            route_data = get_eco_friendly_route(start, end, emission_type)
            routes = route_data["routes"]
            for route in routes:
                # path = route["overview_polyline"]["points"]
                path = route["polyline"]["encodedPolyline"]
                literusage = route["travelAdvisory"]["fuelConsumptionMicroliters"]
                meters = route["distanceMeters"]
                microliters = float(literusage)
                gallonusage = microliters/3785000
                miles = float(meters)/1609.344
                coordinates = decode_polyline(path)
                comb07_value = miles/gallonusage
                seconds = route["duration"]
                # Convert coordinates to list of dictionaries
                coords_list = [{"lat": coord[0], "lon": coord[1]} for coord in coordinates]
                    
                # Display route on map
                st.map(coords_list)
                st.title("Usage: " + str(gallonusage) + "g")
                st.title("Distance: " + str(miles) + " mi.")
                st.title("True Usage: " + str((gallonusage/(1/comb07_value))*(1/comb08_value)))
                st.title("Duration: " + str(seconds) + "ec")
        except Exception as e:
            st.error("An error occurred: {}".format(e))
    else:
        st.warning("Please enter a starting point and destination.")

if __name__ == "__main__":
    main()
