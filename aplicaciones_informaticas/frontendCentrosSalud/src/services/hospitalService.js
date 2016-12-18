import { baseUri } from './constants';

const hospitalService = {
  getHospitals () {
    console.log(baseUri);
    const uri = baseUri + '/healthcenters/';
    const options = {
      method: 'GET',
      mode: 'cors',
    };

    return fetch(uri, options)
      .then(result => result.json());
  }
};

export default hospitalService;