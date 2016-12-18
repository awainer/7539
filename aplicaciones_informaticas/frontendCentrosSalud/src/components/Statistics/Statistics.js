import React, { Component } from 'react';
import { feedService, hospitalService } from '../../services';
import Dropdown from 'react-toolbox/lib/dropdown';

class Statistics extends Component {

  constructor(props){
	  super(props);
	  this.state = { healthCenters: [] };
	  this.handleHealthcenterChange = this.handleHealthcenterChange.bind(this);
  }


  componentDidMount () {
    hospitalService.getHospitals()
      .then(result => this.setState({ healthCenters: result.results }));
  }

  handleHealthcenterChange (value) {
    const retrieveFeed = () => {
      return feedService.getFeed(value)
      .then(result => {
        const timerId = setTimeout(retrieveFeed, 2000);
        const newResult = [].concat(result, this.state.feedResults);
        this.setState({ timerId, feedResults: newResult });
      });
    };
  }

  render () {
    return (
      <div className="rate">
        <Dropdown
          auto
          allowBlank={true}
          label='Seleccione hospital'
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthcenterId}
        />
      </div>
    );
  }
}
export default Statistics;


