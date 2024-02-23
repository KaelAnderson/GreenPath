import React from 'react';
import { useState, useEffect } from 'react';
//import axios from 'axios'; // assuming we'll use it (?)
import './App.css';
import './index.css';
const google = window.google;


function App() {
  const [genMap, setGenMap] = useState(1);

  const handleGenMap = (event) => {
    setGenMap((prev) => prev * -1);
  }

  useEffect(() => {
    let map;

    async function initMap() {
      // The location of Uluru
      const position = { lat: -25.344, lng: 131.031 };
      // Request needed libraries.
      //@ts-ignore
      const { Map } = await google.maps.importLibrary("maps");
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
    }

    initMap();
  }, [genMap]);
  //perhaps regen map when destination state is updated using a useeffect hook


  return (
    <div className="App">
      
      <h1>hello greepath nation</h1>
      <button onClick={handleGenMap}>Generate Map</button>
      <div id="mapDiv">

      </div>
    </div>
  
    );
  }

export default App;