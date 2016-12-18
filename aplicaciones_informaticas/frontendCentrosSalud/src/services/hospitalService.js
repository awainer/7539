const baseUri = 'http://192.168.5.20:8000/api/v1/healthcenters/';

const hospitalService = {
  getHospitals (hospital) {
    const options = {
      method: 'GET',
      mode: 'cors',
    };

    return fetch(baseUri, options)
      .then(result => result.json());
  }
};

export default hospitalService;