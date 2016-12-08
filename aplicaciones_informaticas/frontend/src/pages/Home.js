import React, { Component } from 'react';
import AppComponents from '../components';

class Home extends Component {

  constructor (props) {
    super(props);
    this.state = { componentToDisplay: null };
    this.displayComponent = this.displayComponent.bind(this);
  }

  displayComponent(component) {
    this.setState({ componentToDisplay: component });
  }

  render () {
    return (
      <div className="home">
        <div className="header">
          <a onClick={() => this.displayComponent(<AppComponents.Recommendation />)}>Recomendación de hospital</a>
          <a onClick={() => this.displayComponent(<AppComponents.GeneralStatistics />)}>Estadísticas de hospitales</a>
          <a onClick={() => this.displayComponent(<AppComponents.HospitalStatistics />)}>Estadísticas generales</a>
        </div>
        <div className="body">
          {this.state.componentToDisplay}
        </div>
      </div>
    );
  }
};


export default Home;