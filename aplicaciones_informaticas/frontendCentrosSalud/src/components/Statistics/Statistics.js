import React, { Component } from 'react';
import { hospitalService, staticsService } from '../../services';
import Dropdown from 'react-toolbox/lib/dropdown';
import { Button } from 'react-toolbox/lib/button';

class Statistics extends Component {

    constructor (props) {
        super(props);
        this.state = { healthCenters: [] };
        this.handleHealthCenterChange = this.handleHealthCenterChange.bind(this);
    }

    componentDidMount () {
        hospitalService.getHospitals().then(result => this.setState({ healthCenters: result.results }));

        var url = "http://localhost:8000/foo";
        var el = document.createElement('script');
        el.src = url.replace('<id>', this.props.embedId);
        this.getDOMNode().appendChild(el);

    }

    handleHealthCenterChange (value) {
        this.setState({ selectedHealthCenterId: value });
    }


    render () {
        return (
            <div>
                Estadísticas por Centro de Salud
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
