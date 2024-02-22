import streamlit as st
import pandas as pd
import numpy as np
import json
import requests

# Streamlit layout
st.title("Google Maps API with Streamlit")
st.write("Simple example to display Google Maps")

# Google Maps API Key
API_KEY = "AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo"

# Define a function to display the map
def display_map(latitude, longitude, zoom_level):
    # Create a URL for the Google Static Maps API
    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{latitude},{longitude}",
        "zoom": zoom_level,
        "size": "800x500",
        "key": API_KEY,
    }
    
    # Display the map image
    st.image(requests.get(url, params=params).content)

# Sidebar inputs
st.sidebar.header("Map Settings")
latitude = st.sidebar.number_input("Latitude", value=37.7749)
longitude = st.sidebar.number_input("Longitude", value=-122.4194)
zoom = st.sidebar.slider("Zoom Level", min_value=1, max_value=20, value=10)

# Display the map
display_map(latitude, longitude, zoom)
