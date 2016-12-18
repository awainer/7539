import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import FontIcon from 'react-toolbox/lib/font_icon';
import styles from './index.css';
import Pacientes from './pages/Pacientes';

class App extends Component {
  render() {
    return (
      <div className={styles.app}>
        <div className={styles.appHeader}>
          <FontIcon className={styles.appLogo} value="add_location" />
          <h3>guardiaApp</h3>
        </div>
        <div className={styles.appIntro}>
          <Pacientes />
        </div>
      </div>
    );
  }
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
