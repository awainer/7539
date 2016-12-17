const geolocationService = {
  getCurrentPosition: () => {
    if (!navigator.geolocation) {
      console.error('You are using a browser with no geolocation!');
      return;
    }

    return new Promise((resolve, reject) => {
      const success = (position) => resolve(position);
      const error = (error) => console.log(`Geolocation failed. Reason: ${error.message}`) && reject(error);

      navigator.geolocation.getCurrentPosition(success, error);
    });
  }
};

export default geolocationService;