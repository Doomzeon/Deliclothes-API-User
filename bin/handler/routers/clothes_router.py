from bin.controller.clothes_controller_new import ClothesController
from flask import request, Response
from bin.services.zara_new import Zara
import json
import bin.utils.logger as logger

_logger = logger.Logger()

import logging

class ClothesRouter:
    def __init__(self, app):
        self.app = app

        # Add decorator to check AUTH

        @app.route('/api_v1/clothes/home_page_posters', methods=['GET'])
        def get_home_page_posters():
            try:
                logging.info('Processing request /api_v1/clothes/home_page_posters')
                clothes_controller = ClothesController(
                    offset=request.args.get("offset"), size=request.args.get("size"))
                return clothes_controller.home_page_posters()
            except Exception as e:
                _logger.log(e, logger.LogLevel.error,
                            message=f'An error occured /api_v1/clothes/home_page_posters')

        @app.route('/api_v1/clothes/<gender>/select/<brand>/<type_clothes>/<id_user>/<language>', methods=['GET'])
        def get_clothes_by_gender_and_type(gender, brand, type_clothes, id_user, language):
            try:
                logging.info(f'Processing request /api_v1/clothes/{gender}/select/{brand}/{type_clothes}/{id_user}/{language}')
                clothes_controller = ClothesController(
                    offset=request.args.get("offset"), size=request.args.get("size"))
                if id_user == 0:
                    return clothes_controller.clothes_list(type_clothes=type_clothes, gender=gender, brand=brand, language=language)
                else:
                    return clothes_controller.clothes_list(type_clothes=type_clothes, gender=gender, id_user=id_user, brand=brand, language=language)

            except Exception as e:
                _logger.log(e, logger.LogLevel.error,
                            message=f'An error occured on /api_v1/clothes/<gender>/select/<brand>/<type_clothes>/<id_user>')

        @app.route('/api_v1/clothes/<brand>/<product_id>/select_similar/<id_user>/<language>', methods=['GET'])
        def get_similar_clothes(brand, product_id, id_user,language):
            try:
                logging.info(f'Processing request /api_v1/clothes/{brand}/{product_id}/select_similar/{id_user}/{language}')
                clothes_controller = ClothesController(
                    offset=request.args.get("offset"), size=request.args.get("size"))
                if id_user is not None:
                    return clothes_controller.similar_clothes(product_id=product_id, brand=brand, id_user=id_user, language= language)
                else:
                    return clothes_controller.similar_clothes(product_id=product_id, brand=brand, language=language)
            except Exception as e:
                _logger.log(e, logger.LogLevel.error,
                            message=f'An error occured /api_v1/clothes/<brand>/<product_id>/select_similar/<id_user>')

        @app.route('/api_v1/clothes/<brand>/<product_id>/select_recomended/<id_user>/<language>', methods=['GET'])
        def get_recomended_clothes(brand, product_id, id_user,language):
            try:
                logging.info(f'Processing request /api_v1/clothes/<{brand}>/<{product_id}>/select_recomended/<{id_user}>/<{language}>')
                
                clothes_controller = ClothesController(
                    offset=request.args.get("offset"), size=request.args.get("size"))
                if id_user is not None:
                    return clothes_controller.recomended_clothes(product_id=product_id, brand=brand, id_user=id_user, language=language)
                else:
                    return clothes_controller.recomended_clothes(product_id=product_id, brand=brand, language=language)

            except Exception as e:
                _logger.log(e, logger.LogLevel.error,
                            message=f'An error occured /api_v1/clothes/<brand>/<product_id>/select_recomended/<id_user>')
                
                
        @app.route('/api_v1/clothe/<product_id>/<brand>/<id_user>/<language>', methods=['GET'])
        def get_clothe_info(product_id, brand , id_user,language):
            try:
                logging.info(f'Processing request /api_v1/clothe/<{product_id}>/<{brand}>/<{id_user}>/<{language}>')
                
                clothes_controller = ClothesController(
                    offset=request.args.get("offset"), size=request.args.get("size"))
                return clothes_controller.clothe_info(product_id=product_id, brand=brand, id_user=id_user, language=language)
            except Exception as e:
                _logger.log(e, logger.LogLevel.error,
                            message=f'An error occured /api_v1/clothes/<brand>/<product_id>/select_similar/<id_user>')
                
                
