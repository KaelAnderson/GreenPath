import React from 'react';
import axios from 'axios'; // assuming we'll use it (?)
import './App.css';
import './index.css';
const google = window.google
function App() {
  let map;

  async function initMap() {
    console.log("hello");
    // The location of Uluru
    const position = { lat: -34.397, lng: 150.644 };
    // Request needed libraries.
    //@ts-ignore
    const { Map, Polyline } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
      zoom: 4,
      center: position,
      mapId: "DEMO_MAP_ID",
    });

    // The marker, positioned at Uluru
    const marker = new AdvancedMarkerElement({
      map: map,
      position: position,
      title: "Uluru",
    });

    //var decodedPath = google.maps.geometry.encoding.decodedPath("ipkcFfichVnP@j@BLoFVwM{E?");
    /*var decodedPath = "ipkcFfichVnP@j@BLoFVwM{E?";
    const polyline = new google.maps.Polyline({
      path: decodedPath,
      strokeColor: "#4285f4",
      strokeOpacity: 1.0,
      strokeWeight: 6,
      map : map
    });
    */
    //const axios = require('axios');

    const polylinePath = [
      {lat: -34.397, lng: 150.644},
      {lat: -34.390, lng: 150.650},
      // Add as many points as you need to create your polyline
    ];
  
    const polyline = new google.maps.Polyline({
      path: polylinePath,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2,
    });

const data = {
  origin: {
    location: {
      latLng: {
        latitude: 37.419734,
        longitude: -122.0827784
      }
    }
  },
  destination: {
    location: {
      latLng: {
        latitude: 37.417670,
        longitude: -122.079595
      }
    }
  },
  travelMode: "DRIVE",
  routingPreference: "TRAFFIC_AWARE",
  departureTime: "2023-10-15T15:01:23.045123456Z",
  computeAlternativeRoutes: false,
  routeModifiers: {
    avoidTolls: false,
    avoidHighways: false,
    avoidFerries: false
  },
  languageCode: "en-US",
  units: "IMPERIAL"
};

const headers = {
  'Content-Type': 'application/json',
  'X-Goog-Api-Key': 'AIzaSyAIG8FuU1bPLh6Z6f9HGAxmDFFevepjpLo',
  'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
};

axios.post('https://routes.googleapis.com/directions/v2:computeRoutes', data, { headers })
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });

  
  }

  initMap();
  //perhaps regen map when destination state is updated using a useeffect hook

 
}



export default App;