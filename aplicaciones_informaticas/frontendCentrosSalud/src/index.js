import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import FontIcon from 'react-toolbox/lib/font_icon';
import styles from './index.css';
import CentroMedico from './pages/CentroMedico';

class App extends Component {
  render() {
    return (
      <div className={styles.app}>
        <div className={styles.appHeader}>
          <FontIcon className={styles.appLogo} value="add_location" />
          <div>
            <h3>guardiaApp</h3>
            <h3>Centro de Salud</h3>
          </div>
        </div>
        <div className={styles.appIntro}>
          <CentroMedico />
        </div>
      </div>
    );
  }
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
