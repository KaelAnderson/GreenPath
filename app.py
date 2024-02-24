import streamlit as st
import requests
import polyline
import json
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
    st.title("Eco-Friendly Route Planner")

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
                    coordinates = decode_polyline(path)
                    
                    # Convert coordinates to list of dictionaries
                    coords_list = [{"lat": coord[0], "lon": coord[1]} for coord in coordinates]
                    
                    # Display route on map
                    st.map(coords_list)
                    st.title("Usage: " + literusage + "µL")
            except Exception as e:
                st.error("An error occurred: {}".format(e))
        else:
            st.warning("Please enter a starting point and destination.")

if __name__ == "__main__":
    main()