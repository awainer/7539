const baseUri = 'http://192.168.5.20:8000/api/v1/hospitals/recommendation';

const specialties = [
  { name: "Clínica", id: 1 },
  { name: "Pediatría", id: 2 },
  { name: "Odontología", id: 3 },
  { name: "Cirugía", id: 4 },
  { name: "Traumatología", id: 5 },
  { name: "Oftalmología", id: 6 },
];

const triageScale = [
  { name: "Atención inmediata (0 minutos de espera).", id: 1 },
  { name: "Atención muy urgente (10 minutos de espera).", id: 2 },
  { name: "Atención urgente (60 minutos de espera).", id: 3 },
  { name: "Atención normal (120 minutos de espera).", id: 4 },
  { name: "Atención no urgente (120 minutos de espera).", id: 5 },
];

const recommendationService = {

  getSpecialties () {
    return new Promise((resolve, reject) => resolve(specialties));
  },

  getTriageScales () {
    return new Promise((resolve, reject) => resolve(triageScale));
  },

  getRecommendation (recommendationOptions) {
    const options = {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify(recommendationOptions),
    };

    return fetch(baseUri, options)
      .then(result => result.json());
  },

  acceptRecommendation (recommendation, triageScale) {
    const eta = new Date(); // now
    eta.setSeconds(new Date().getSeconds() + recommendation.travelTime + recommendation.waitTime);

    const options = {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify({
        triageScale: 1,
        eta: eta.toISOString()
      }),
    };

    const url = baseUri + `/select/${recommendation.hc_id}/queue/${recommendation.queue_id}/`;
    return fetch(url, options)
      .then(result => result.json());
  }
};

export default recommendationService;