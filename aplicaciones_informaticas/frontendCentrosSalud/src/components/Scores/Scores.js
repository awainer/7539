import React, { Component } from 'react';
import { hospitalService  } from '../../services';

import Dropdown from 'react-toolbox/lib/dropdown';
import FontIcon from 'react-toolbox/lib/font_icon';

import styles from './styles.css'

class Scores extends Component {

  constructor (props) {
    super(props);
    this.state = { healthCenters: [], hospitalScore: null, currentScore: 0 };
    this.handleHealthcenterChange = this.handleHealthcenterChange.bind(this);
  }

  componentDidMount () {
    hospitalService.getHospitals()
      .then(result => this.setState({ healthCenters: result.results }));
  }

  handleHealthcenterChange (value) {
    if (this.state.timerId) {
      clearTimeout(this.state.timerId);
    }
    
    this.setState({ selectedHealthcenterId: value, hospitalScore: 5, currentScore: 0 });    
  }

  render () {
    const getStars = ({ratingValue, maxRating}) => {
      const items = [];

      for (let i = 0; i < ratingValue; i++) {
        items.push(<FontIcon key={i} className={`${styles.ratingStar} ${styles.highlight}`} value='star' />);
      }

      for (let i = ratingValue; i < maxRating; i++) {
        items.push(<FontIcon className={styles.ratingStar} key={i} value='star' />);
      }

      return items;
    }

    return (
      <div className={styles.Scores}>
        
        <Dropdown
          auto
          allowBlank={true}
          label='Seleccione hospital'
          onChange={this.handleHealthcenterChange}
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthcenterId}
        />
        
       </div>      
    );
  }
}

export default Scores;
