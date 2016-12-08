const baseUri = 'http://192.168.5.20:8000/api/v1/hospitals/recommendation';

const recommendationService = {
  getRecommendation (recommendationOptions) {
    var options = {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify(recommendationOptions),
    };

    return fetch(baseUri, options)
      .then(result => result.json())
  }
};

export default recommendationService;