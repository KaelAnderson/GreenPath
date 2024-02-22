import React from 'react';
import axios from 'axios'; // assuming we'll use it (?)
import './App.css';
import './index.css';


function App() {


return (
  <div className="App">
    <h1>hello greepath nation</h1>
  </div>
  );

  const params = {
    origin: {
      location: {
        latLng: {
          latitude: -37.8167,
          longitude: 144.9619
        }
      }
    },
    destination: {
      location: {
        latLng: {
          latitude: -37.8155,
          longitude: 144.9663
        }
      }
    },
    routingPreference: "TRAFFIC_AWARE",
    travelMode: "DRIVE"
  };
  
  const apiKey = "YOUR_API_KEY";
  
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Goog-Api-Key": apiKey,
      "X-Goog-FieldMask": "routes.route_token,routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    },
    body: JSON.stringify(params)
  };
  
  fetch("https://routes.googleapis.com/directions/v2:computeRoutes", requestOptions)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log("Error:", error));
}

export default App;