import React, { Component } from 'react';
import { Recommendation, Scores, RealTimeMap } from '../../components';
import { Tab, Tabs } from 'react-toolbox/lib/tabs';

class HomePacientes extends Component {

  constructor (props) {
    super(props);
    this.state = { tabIndex: 0 };

    this.displayComponent = this.displayComponent.bind(this);
    this.handleFixedTabChange = this.handleFixedTabChange.bind(this);
  }

  displayComponent (component) {
    this.setState({ componentToDisplay: component });
  }

  handleFixedTabChange (tabIndex) {
    this.setState({ tabIndex: tabIndex });
  }

  render () {
    return (
      <div className="Pacientes">
        <Tabs index={this.state.tabIndex} onChange={this.handleFixedTabChange} fixed>
          <Tab label="Recomendación de Hospitales">
            <Recommendation />
          </Tab>
          <Tab label="Mapa en Tiempo Real">
            <RealTimeMap />
          </Tab>
          <Tab label="Calificar Centros Médicos">
            <Scores />
          </Tab>
        </Tabs>
      </div>
    );
  }
};


export default HomePacientes;
