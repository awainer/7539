const baseUri = 'http://localhost:8000/api/v1/hospitals'

const feedService = {
  getFeed (hospitalId) {
    const uri = baseUri + `/${hospitalId}/feed`;
    const options = {
      method: 'GET',
      mode: 'cors',
    };

    return fetch(uri, options)
      .then(result => result.json());
  }
};

export default feedService;
