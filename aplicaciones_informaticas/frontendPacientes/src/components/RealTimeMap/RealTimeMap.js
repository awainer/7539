import React, { Component } from 'react';

class RealTimeMap extends Component {


  render () {
    return (
        <div className="embed-container">
        <p><a href="http://localhost:8000/static/map.html">Abrir en nueva ventana</a></p>
        <iframe src="http://localhost:8000/static/map.html" height="400"/>
        </div>
    );
  }
}

export default RealTimeMap;
