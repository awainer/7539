import React, { Component } from 'react';
import { hospitalService, scoreService  } from '../../services';

import Dropdown from 'react-toolbox/lib/dropdown';
import { Button } from 'react-toolbox/lib/button';
import { Slider } from 'react-toolbox/lib/slider';
import Input from 'react-toolbox/lib/input';

import styles from './styles.css'

class Scores extends Component {

  constructor (props) {
    super(props);
    this.state = { healthCenters: [], slider: 0 };
    this.handleHealthcenterChange = this.handleHealthcenterChange.bind(this);
  }

  componentDidMount () {
    hospitalService.getHospitals()
      .then(result => this.setState({ healthCenters: result.results }));
  }

  handleHealthcenterChange (value) {
    this.setState({ selectedHealthcenterId: value, currentScore: 0 });    
  }

  handleSliderChange = (value) => {
    this.setState({'slider': value});
  };
  
  submit = ()  => {
	console.log (this.state.slider);
	scoreService.rateHospital(this.state.slider, this.state.selectedHealthcenterId);
  };

  render () {
  
    return (
      <div className=''>        
      
        <Dropdown
          auto
          allowBlank={true}
          label='Seleccione hospital'
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthcenterId}
          onChange={this.handleHealthcenterChange}
        />
      
        <div className={styles.scoreSelection}>
           <Input
              type='text'
              label='Puntuar Centro Médico: '
              name='rate'
            />
        </div>
		

		<Slider pinned snaps min={0} max={5} step={1} 
			editable value={this.state.slider}
			onChange={this.handleSliderChange}
		/>

		<Button icon='inbox' label='Enviar calificación' flat onMouseUp={this.submit.bind(this)} />
       
       </div>      
    );
  }
}

export default Scores;
