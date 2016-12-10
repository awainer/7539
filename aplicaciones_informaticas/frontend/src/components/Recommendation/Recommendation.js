import React, { Component } from 'react';
import { geolocationService, recommendationService } from '../../services';

import { Button } from 'react-toolbox/lib/button';
import Dropdown from 'react-toolbox/lib/dropdown';
import Input from 'react-toolbox/lib/input';

import styles from './Recommendation.css';

class Recommendation extends Component {

  constructor (props) {
    super(props);
    this.state = { specialties: [], triageScales: [], recommendationResults: [], selectedGeo: { latitude: -34.63, longitude: -58.48} };

    this.handleSpecialtyChange = this.handleSpecialtyChange.bind(this);
    this.handleTriageScaleChange = this.handleTriageScaleChange.bind(this);
    this.handleGeoLatitudeChange = this.handleGeoLatitudeChange.bind(this);
    this.handleGeoLongitudeChange = this.handleGeoLongitudeChange.bind(this);

    this.getRecommendation = this.getRecommendation.bind(this);
    this.calculateGeo = this.calculateGeo.bind(this);
  }

  componentDidMount () {

    recommendationService.getSpecialties()
      .then(result => this.setState({ specialties: result, selectedSpecialtyId: result[0].id }));

    recommendationService.getTriageScales()
      .then(result => this.setState({ triageScales: result, selectedTriageScaleId: result[0].id }));
  }

  handleSpecialtyChange (value) {
    this.setState({ selectedSpecialtyId: value });
  }

  handleTriageScaleChange (value) {
    this.setState({ selectedTriageScaleId: value });
  }

  handleGeoLatitudeChange (value) {
    this.setState({ selectedGeo: { latitude: value } });
  }

  handleGeoLongitudeChange (value) {
    this.setState({ selectedGeo: { longitude: value } });
  }

  calculateGeo () {
    geolocationService.getCurrentPosition()
      .then(result => this.setState({ selectedGeo: result.coords }));
  }

  getRecommendation () {
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
      <div className={styles.recommendation}>

        <div className={styles.recommendationForm}>
          <div className="specialties">
            <Dropdown
              auto
              allowBlank={true}
              label='Seleccione especialidad'
              onChange={this.handleSpecialtyChange}
              source={this.state.specialties.map(item => ({ value: item.id, label: item.name }))}
              value={this.state.selectedSpecialtyId}
            />
          </div>

          <div className="triageScale">
            <Dropdown
              auto
              allowBlank={true}
              label='Seleccione urgencia'
              onChange={this.handleTriageScaleChange}
              source={this.state.triageScales.map(item => ({ value: item.id, label: item.name }))}
              value={this.state.selectedTriageScaleId}
            />
          </div>

          <div className={styles.currentPosition}>
            <Input
              type='text'
              label='Seleccione latitud'
              name='geo'
              value={this.state.selectedGeo.latitude}
              onChange={this.handleGeoLatitudeChange}
            />
            <Input
              type='text'
              label='Seleccione longitud'
              name='geo'
              value={this.state.selectedGeo.longitude}
              onChange={this.handleGeoLongitudeChange}
            />
            <Button
              icon='my_location'
              onClick={this.calculateGeo}
              floating accent mini
            />
          </div>

          <Button
            className={styles.locationButton}
            icon='add_location'
            label='Buscar recomendaciones'
            raised
            primary
            onClick={this.getRecommendation}
          />
        </div>

        <div className={styles.recommendationResults}>
        {
          this.state.recommendationResults.map(result => (
           <p>{result.name}</p>
          ))
        }
        </div>
      </div>
    );
  }
}

export default Recommendation;


