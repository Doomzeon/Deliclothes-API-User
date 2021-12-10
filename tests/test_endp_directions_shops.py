import unittest
from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.controller.user_controller import UsernameController
from bin.services.mapbox import MapBox
import logging
shops_lat_lng = [
    {
        "lat": 9.1858432,
        "lng": 45.4723719,
    },
    {
        "lat": 9.1770885,
        "lng": 45.4723719,
    },
    {
        "lat": 45.4660216,
        "lng": 9.2216775,
    }
]



def test_delivery_directions(caplog):
    with caplog.at_level(logging.DEBUG):
        response = MapBox().calculate_directions(lat_lng_list= shops_lat_lng)
        assert True == False


