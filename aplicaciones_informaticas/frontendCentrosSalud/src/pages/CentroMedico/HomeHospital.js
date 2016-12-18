import React, { Component } from 'react';
import { Feed, Statistics } from '../../components';
import { Tab, Tabs } from 'react-toolbox/lib/tabs';

import styles from './HomeHospital.css';

class HomeHospital extends Component {

  constructor (props) {
    super(props);
    this.state = { tabIndex: 0 };

    this.handleTabChange = this.handleTabChange.bind(this);
  }

  handleTabChange (value) {
    this.setState({ tabIndex: value });
  }

  render () {
    return (
      <div className={styles.home}>
        <Tabs index={this.state.tabIndex} onChange={this.handleTabChange} fixed>
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
