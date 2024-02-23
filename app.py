import streamlit as st
try:
    import googlemaps
except ImportError:
    st.warning("Installing required package... Please wait!")
    import subprocess
    subprocess.run(["pip", "install", "googlemaps"])
    import googlemaps

from datetime import datetime
import polyline
import pandas as pd

# Google Maps API Key (replace with your own key)
API_KEY = "AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo"

# Create a Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

# Streamlit App
def main():
    st.title("Google Maps Route Drawing App")
    
    # Input boxes for origin and destination
    origin = st.text_input("Enter Origin (e.g., 'New York City'):")
    destination = st.text_input("Enter Destination (e.g., 'Los Angeles'):")
    
    # Button to draw the route
    if st.button("Draw Route"):
        if not origin or not destination:
            st.warning("Please enter both origin and destination.")
        else:
            # Get directions
            directions_result = gmaps.directions(origin, destination, mode="driving")
            
            if len(directions_result) == 0:
                st.warning("No route found. Please check your inputs.")
            else:
                for i, route in enumerate(directions_result):
                    st.subheader(f"Route {i+1}")
                    # Extract route coordinates
                    overview_polyline = route['overview_polyline']['points']
                    decoded_route = polyline.decode(overview_polyline)
                    # Create DataFrame with 'latitude' and 'longitude' columns
                    df = pd.DataFrame(decoded_route, columns=['latitude', 'longitude'])
                    # Display map with route
                    st.map(df)
                    # Optional: Print route duration and distance
                    duration = route['legs'][0]['duration']['text']
                    distance = route['legs'][0]['distance']['text']
                    st.write(f"**Duration:** {duration}, **Distance:** {distance}")
                    st.markdown("---")
                
    st.markdown("---")
    st.markdown("Created with ❤️ by Your Name")

if __name__ == "__main__":
    main()
