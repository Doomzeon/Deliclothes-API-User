import datetime
import requests
import logging
import time
from urllib.parse import unquote
import bin.utils.logger as logger

_logger = logger.Logger()


class MapBox:

    def __init__(self) -> None:
        self._acess_token = "pk.eyJ1IjoiZG9vbXplb24iLCJhIjoiY2txbWMwd2ozMDFhYTJ0bWg4YWx1dDR4ayJ9.A9QXry7u_UkUUIkmiS8ivg"
        self._url_direction_cycling = "https://api.mapbox.com/directions/v5/mapbox/cycling/"
        self._url_geocoding = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        self.lng_start_point = "45.480437"
        self.lat_start_point = "9.1852853"

    def calculate_directions(self, lat_lng_list: list):
        try:
            lat_lng_str_concat = self.lat_start_point + "," + self.lng_start_point
            for lat_lng in lat_lng_list:
                lat_lng_str_concat += f";{lat_lng['lng']},{lat_lng['lat']}"
            logging.info(
                f'Contacting -> {self._url_direction_cycling}{lat_lng_str_concat}/?access_token={self._acess_token}')
            response = requests.get(
                f"{self._url_direction_cycling}{lat_lng_str_concat}/?access_token={self._acess_token}")
            logging.info(response.json())
            duration_delivery = time.strftime('%H:%M:%S',  time.gmtime(
                response.json()['routes'][0]['duration']))
            logging.info(duration_delivery)
            return response.json()['routes'][0]['duration'], duration_delivery
        except Exception as e:

            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while calculating directions ')
            raise(e)

    def caluclate_duration_between_2_positions(self, lat1, lng1, lat2, lng2):
        try:
            logging.info(
                F'Trying to calculate duration between 2 position {lat1} {lng1} , {lat2} {lng2}')
            response = requests.get(
                f"{self._url_direction_cycling}{lat1},{lng1};{lat2},{lng2}.json/?access_token={self._acess_token}")
            logging.info(f'Respone from Map box is :{response.json()}')
            print(time.strftime('%H:%M:%S',  time.gmtime(
                response.json()['routes'][0]['duration'])))
            return datetime.datetime.strptime(time.strftime('%H:%M:%S',  time.gmtime(response.json()['routes'][0]['duration'])), '%H:%M:%S').time()

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while calculating duration between 2 positions ')
            raise(e)

    def get_lat_lng_of_position(self, street_name, country, city):
        try:
            logging.info(
                f'Trying to get position of {street_name} {country} {city}')
            response = requests.get(
                f"{self._url_geocoding}{unquote(street_name+' '+city+' '+country )}.json/?access_token={self._acess_token}")
            logging.info(f'Respone from Map box is :{response.json()}')
            lat = response.json()['features'][0]['center'][0]
            lng = response.json()['features'][0]['center'][1]
            return lat, lng
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while geting at lng position by street name... ')
            raise(e)
