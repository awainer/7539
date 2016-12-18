import React, { Component } from 'react';
import { Feed, Statistics } from '../../components';
import { Tab, Tabs } from 'react-toolbox/lib/tabs';

class HomeHospital extends Component {

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
      <div className="CentroMedico">
        <Tabs index={this.state.tabIndex} onChange={this.handleFixedTabChange} fixed>
          <Tab label="Feed">
            <Feed />
          </Tab>
          <Tab label="Estadísticas">
            <Statistics />
          </Tab>
        </Tabs>
      </div>
    );
  }
};


export default HomeHospital;
