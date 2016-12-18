const baseUri = 'http://192.168.5.20:8000';

const scoreService = {
  rateHospital (rate,hospital) {
   const options = {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify({
        rating: rate
      }),
    };

    const url = baseUri + `/api/v1/hospitals/${hospital}/rate`;
    return fetch(url, options)
      .then(result => result.json());
  }

};

export default scoreService;
