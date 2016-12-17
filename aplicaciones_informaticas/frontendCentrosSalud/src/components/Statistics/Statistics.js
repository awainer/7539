import React, { Component } from 'react';

class Statistics extends Component {

  constructor(){
	  super(props);
	  this.state = { healthCenters: [] };
	  this.handleHealthcenterChange = this.handleHealthcenterChange.bind(this);	      
  }
  render () {
    return (
      <div className="rate">
        statistics!
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
export default Statistics;


