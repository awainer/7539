
import googlemaps
from datetime import datetime
from . import geo_settings


class GeoDistance():
    def __init__(self):
        self.gmaps = googlemaps.Client(key=geo_settings.api_key)
        pass

    def get_travel_time_and_distance(self, point_a, point_b):
        now = datetime.now()
        response = self.gmaps.directions(point_a, point_b, mode="transit", departure_time=now)

        print(geo_settings.api_key, point_a, point_b)
        duration_in_seconds = response[0]['legs'][0]['duration']['value']
        distance_in_meters = response[0]['legs'][0]['distance']['value']
        return duration_in_seconds, distance_in_meters

if __name__ == '__main__':
    c = GeoDistance()
    pa = (-34.617599, -58.368157)
    pb = (-34.6288473603882, -34.6288473603882)
    import pprint
    pprint.pprint(c.get_travel_time_and_distance(pa, pb))
