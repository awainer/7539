import React, { Component } from 'react';
import { geolocationService, recommendationService } from '../services';

const specialties = [
  { name: "Clínica", id: 1 },
  { name: "Pediatría", id: 2 },
  { name: "Odontología", id: 3 },
  { name: "Cirugía", id: 4 },
  { name: "Traumatología", id: 5 },
  { name: "Oftalmología", id: 6 },
];

const triageScale = [
  { name: "A", id: 1 },
  { name: "B", id: 2 },
  { name: "C", id: 3 },
  { name: "D", id: 4 },
  { name: "E", id: 5 },
];

class Recomendation extends Component {

  constructor (props) {
    super(props);
    this.state = {
      selectedSpecialtyId: specialties[2].id,
      selectedTriageScaleId: triageScale[2].id,
      selectedGeo: { latitude: null, longitude: null },
      recommendationResults: [],
    };

    this.handleSpecialtyChange = this.handleSpecialtyChange.bind(this);
    this.handleTriageScaleChange = this.handleTriageScaleChange.bind(this);
    this.getRecommendation = this.getRecommendation.bind(this);
  }

  componentDidMount () {
    geolocationService.getCurrentPosition()
      .then((result) => {
        this.setState({ selectedGeo: result.coords });
      });
  }

  handleSpecialtyChange (event) {
    this.setState({ selectedSpecialtyId: parseInt(event.target.value, 10) });
  }

  handleTriageScaleChange (event) {
    this.setState({ selectedTriageScaleId: parseInt(event.target.value, 10) });
  }

  getRecommendation() {
    const values = {
      "latitude": this.state.selectedGeo.latitude,
      "longitude": this.state.selectedGeo.longitude,
      "specialty": this.state.selectedSpecialtyId,
      "triageScale": this.state.selectedTriageScaleId,
    };

    return recommendationService.getRecommendation(values)
      .then((results) => this.setState({ recommendationResults: results }));
  }

  render () {
    return (
      <div className="recommendation">

        <div className="specialties">
          <label>Especialidad:</label>
          <select onChange={this.handleSpecialtyChange} value={this.state.selectedSpecialtyId}>
            {
              specialties.map(item => (
                <option key={item.id} value={item.id}>{item.name}</option>
              ))
            }
          </select>
        </div>

        <div className="triageScale">
          <label>Severidad:</label>
          <select onChange={this.handleTriageScaleChange} value={this.state.selectedTriageScaleId}>
            {
              triageScale.map(item => (
                <option key={item.id} value={item.id}>{item.name}</option>
              ))
            }
          </select>
        </div>

        <div className="currentPosition">
          <label>Posición actual:</label>
          <span>
          {
            this.state.selectedGeo.latitude ?
            `Latitud: ${this.state.selectedGeo.latitude} -
             Longitud: ${this.state.selectedGeo.longitude}
             (más o menos ${this.state.selectedGeo.accuracy} metros)`
             : ''
          }
          </span>
        </div>

        <button onClick={this.getRecommendation}>Buscar</button>
        {
          this.state.recommendationResults.map(result => (
           <p>{result.name}</p>
          ))
        }
      </div>
    );
  }
}

export default Recomendation;


