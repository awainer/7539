import { baseUri } from './constants';

const feedService = {
  getFeed (hospitalId) {
    const uri = baseUri + `/hospitals/${hospitalId}/feed`;
    const options = {
      method: 'GET',
      mode: 'cors',
    };

    return fetch(uri, options)
      .then(result => result.json());
  }
};

export default feedService;