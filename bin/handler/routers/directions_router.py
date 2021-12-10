
from bin.controller.directions_controller import DirectionsController
from flask import request, Response
import json
import bin.utils.logger as logger

_logger = logger.Logger()

import logging

class DirectionsRouter:
    def __init__(self, app):
        self.app = app

        @app.route('/api_v1/dir/order_get_times_unavailable/<id_user>', methods=['GET'])
        def get_dir(id_user):
            print(id_user)
            return DirectionsController().calculate_unavailable_times(id_user= id_user)
            