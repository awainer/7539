import React, { Component } from 'react';
import { hospitalService } from '../../services';
import Dropdown from 'react-toolbox/lib/dropdown';
import { Button } from 'react-toolbox/lib/button';

var DatePicker = require('react-datepicker');
var moment = require('moment');

require('react-datepicker/dist/react-datepicker.css');

class Statistics extends Component {

  constructor (props) {
    super(props);
    let currentDate = moment();
    this.state = { healthCenters: [], startDate:currentDate, endDate:currentDate };
    this.handleHealthCenterChange = this.handleHealthCenterChange.bind(this);
  }

    componentDidMount () {
        hospitalService.getHospitals().then(result => this.setState({ healthCenters: result.results }));
    }

    handleHealthCenterChange (value) {
        this.setState({ selectedHealthCenterId: value });
    }

  handleStartDateChange (date) {
    this.setState({
      startDate: date
    });
  }

  handleEndDateChange (date) {
    this.setState({
      endDate: date
    });
  }

  render () {
	
	let url = "http://localhost:8000/static/chart.html?hc_id=";
	url += this.state.selectedHealthCenterId;
	url += "&dateFrom=" + this.state.startDate.toISOString();
	url += "&dateTo=" + this.state.endDate.toISOString();

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

        <div className="react-datepicker">
            <DatePicker
            selected={this.state.startDate}
            onChange={this.handleStartDateChange}
            />
        </div>

        <div className="react-datepicker">
            <DatePicker
            selected={this.state.endDate}
            onChange={this.handleEndDateChange} />
        </div>

        <Button
          icon="inbox"
          label='Ver Reportes'
          raised
          primary
          disabled={!this.state.selectedHealthCenterId}
          href={url}
          target="_blank"
        />

      </div>
    );
  }
}

export default Statistics;
