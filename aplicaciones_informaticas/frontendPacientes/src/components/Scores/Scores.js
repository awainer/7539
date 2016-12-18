import React, { Component } from 'react';
import { hospitalService, scoreService  } from '../../services';

import Dropdown from 'react-toolbox/lib/dropdown';
import { Button } from 'react-toolbox/lib/button';
import { Slider } from 'react-toolbox/lib/slider';

import styles from './styles.css'

class Scores extends Component {

  constructor (props) {
    super(props);
    this.state = { healthCenters: [], currentScore: 1 };
    this.handleHealthCenterChange = this.handleHealthCenterChange.bind(this);
  }

  componentDidMount () {
    hospitalService.getHospitals()
      .then(result => this.setState({ healthCenters: result.results }));
  }

  handleHealthCenterChange (value) {
    this.setState({ selectedHealthCenterId: value, currentScore: 1 });
  }

  handleSliderChange = (value) => {
    this.setState({ currentScore: value });
  };

  submit = ()  => {
    scoreService.rateHospital(this.state.currentScore, this.state.selectedHealthCenterId);
  };

  render () {

    return (
      <div className={styles.scores}>

        <Dropdown
          auto
          allowBlank={true}
          label="Seleccione hospital"
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthCenterId}
          onChange={this.handleHealthCenterChange}
        />

        <div className={styles.scoreSelection}>
            <span>Puntuar Centro Médico</span>
            <Slider
              editable={this.state.selectedHealthCenterId}
              pinned snaps
              min={1} max={5} step={1}
              value={this.state.currentScore}
              disabled={!this.state.selectedHealthCenterId}
              onChange={this.handleSliderChange}
            />
        </div>

        <Button
          icon="inbox"
          label='Enviar calificación'
          raised
          primary
          disabled={!this.state.selectedHealthCenterId}
          onClick={this.submit}
        />

      </div>
    );
  }
}

export default Scores;
