import React, { Component } from 'react';
import { hospitalService, feedService } from '../../services';

import Dropdown from 'react-toolbox/lib/dropdown';

import styles from './styles.css'

let data = [
  {
    key: "dataSource1",
    values: [
      {label: "A", value: 3},
      {label: "B", value: 4}
    ]
  },
  {
    key: "dataSource2",
    values: [
      {label: "X", value: 7},
      {label: "Y", value: 8}
    ]
  }
];

class Feed extends Component {

  constructor (props) {
    super(props);
    this.state = { healthCenters: [], feedResults: [] };
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

    if (this.state.timerId) {
      clearTimeout(this.state.timerId);
    }

    this.setState({ selectedHealthcenterId: value, feedResults: [] });
    retrieveFeed();
  }

  render () {
    return (
      <div className={styles.feed}>
        <Dropdown
          auto
          allowBlank={true}
          label='Seleccione hospital'
          onChange={this.handleHealthcenterChange}
          source={this.state.healthCenters.map(item => ({ value: item.id, label: item.name }))}
          value={this.state.selectedHealthcenterId}
        />
        <div className={styles.charts}>

        </div>
        <div className={styles.items}>
          {
            this.state.feedResults.map(item => (
              <p key={item.id} className={styles.item}>
                <span>ETA: {item.eta}</span><span> - </span>
                <span>Health center: {item.health_center}</span><span> - </span>
                <span>Queue: {item.queue}</span><span> - </span>
                <span>Triage scale: {item.triageScale}</span>
              </p>
            ))
          }
        </div>
      </div>
    );
  }
}

export default Feed;


