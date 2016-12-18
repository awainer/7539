import React, { Component } from 'react';
import { hospitalService } from '../../services';
import Dropdown from 'react-toolbox/lib/dropdown';

class Statistics extends Component {

  constructor (props) {
    super(props);
    this.state = { healthCenters: [] };
    this.handleHealthCenterChange = this.handleHealthCenterChange.bind(this);
  }

  componentDidMount () {
    hospitalService.getHospitals()
      .then(result => this.setState({ healthCenters: result.results }));
  }

  handleHealthCenterChange (value) {
    this.setState({ selectedHealthCenterId: value });
  }

  render () {

    return (
      <div>
        <Dropdown
          auto
          allowBlank={true}
          label="Seleccione hospital"
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthCenterId}
          onChange={this.handleHealthCenterChange}
        />
      </div>
    );
  }
}

export default Statistics;
