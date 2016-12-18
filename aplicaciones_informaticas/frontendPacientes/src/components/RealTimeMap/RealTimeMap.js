import React, { Component } from 'react';

class RealTimeMap extends Component {


  render () {
    return (
        <div className="embed-container">
        <iframe src="http://localhost:8000/static/map.html" height="500"/>
        </div>
    );
  }
}

export default RealTimeMap;
