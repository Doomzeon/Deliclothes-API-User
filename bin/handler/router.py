from bin.handler.routers.directions_router import DirectionsRouter
from bin.services.mapbox import MapBox
from flask import Flask, request, Response
from bin.handler.routers.clothes_router import ClothesRouter
from bin.handler.routers.username_router_new import UsernameRouter


class Router:
    def __init__(self, app):
        self.app = app

        @app.route('/api_v1/alive', methods=['GET'])
        def alive():
            """Check if the service is running"""
            return "I'm alive!"

        ClothesRouter(app=app)
        UsernameRouter(app=app)
        DirectionsRouter(app=app)
