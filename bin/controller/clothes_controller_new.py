from bin.services.database_new import Database
from flask import Response
import json
from bin.services.zara_new import Zara

import bin.utils.logger as logger
import logging

_logger = logger.Logger()


class ClothesController:

    def __init__(self, offset: int, size: int):
        self._offset = offset
        self._size = size

    def home_page_posters(self):
        try:
            logging.info(f'Selecting home page posters data from Database...')
            posters = Database().select_posters()
            logging.info(f'Selected with success posters: {posters}')
            res = []
            logging.info(f'Procced by processing posters to build reponse...')
            for poster in posters:
                res.append(
                    {"brand": poster.brand, "description": poster.description, "img": poster.image_poster})
            logging.info(f'Proccecs posters with success. Posters: {res}')
            return Response(self.__build_payload_response(message='OK', payload=res), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting home page posters.')
            return Response(self.__build_payload_response(message='Internal server errore'), status=500, mimetype="application/json")

    def clothes_list(self, brand: str, gender: str, type_clothes: str,language:str, id_user: int = None):
        try:
            logging.info(f'Selecing clothes...')
            if type(id_user) is int:
                logging.info(f'Id user is not None. Trying to select gender of the user from DB...')
                gender = Database().select_gender_user(id_user=id_user)
                logging.info(f'Selected with success gender {gender} of the user with id {id_user}')
            logging.info(f'Switching the brand name {brand}....')
            if brand.lower() == 'zara':
                logging.info('Selecing category from shop zara....')
                category = list(filter(lambda item: item['gender'].lower() == gender.lower(
                ) and item['type_name'].lower() == type_clothes.lower(), zara_categories))
                logging.info(F'Selecting clothes from category: {category} ....')
                clothes = Zara(language=language).get_clothes(
                    category_id=category[0]['category_id'], id_user=id_user)
                logging.info(f'Selected with success clothes of category: {clothes}')
                return Response(self.__build_payload_response(message='OK', payload=clothes), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting clothes list from shops.')
            return Response(self.__build_payload_response(message='Internal server errore'), status=500, mimetype="application/json")

    def clothe_info(self, product_id: str, brand: str, language:str, id_user: int = None):
        try:
            # TODO SWITCH BY BRAND
            logging.info(F'Trying to get product info with id {product_id}')
            clothe = Zara(language=language).get_product_info_data(
                id_clothe=product_id, user_liked=False, id_user=id_user)
            return Response(self.__build_payload_response(message='OK', payload=clothe), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting similar clothes.')
            return Response(self.__build_payload_response(message='Internal server errore'), status=500, mimetype="application/json")

    def similar_clothes(self, product_id: int, brand: str,language:str, id_user: int = None):
        try:
            logging.info(f'Selecting similar clothes')
            logging.info(f'Switching the brand name {brand}....')
            if brand.lower() == 'zara':
                logging.info('Selecing category from shop zara....')
                clothes = Zara(language=language).get_similar_clothes(product_id=product_id, id_user=id_user)
                logging.info(
                    f'Selected with success similar clothes {clothes}')
                return Response(self.__build_payload_response(message='OK', payload=clothes), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting similar clothes.')
            return Response(self.__build_payload_response(message='Internal server errore'), status=500, mimetype="application/json")

    def recomended_clothes(self, product_id: int, brand: str,language:str, id_user: int = None):
        try:
            logging.info(f'Trying to select recomended clothes by product_id {product_id}')
            logging.info(f'Switching the brand name {brand}....')
            if brand.lower() == 'zara':
                logging.info(F'Selecting clothes from shop zara')
                clothes = Zara(language=language).get_related_clothes(product_id=product_id, id_user=id_user)
                logging.info(f'Selected with success clothes {clothes}')
                return Response(self.__build_payload_response(message='OK', payload=clothes), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured whiel selecting recomended clothes')
            return Response(self.__build_payload_response(message='Internal server errore'), status=500, mimetype="application/json")

    def __build_payload_response(self, message: str, payload=None) -> dict:
        return json.dumps({
            "message": message,
            "payload": payload
        })


zara_categories = [
    {
        "category_id": 1882210,
        "type_name": 'Jackets',
        "gender": 'Woman'
    },
    {
        "category_id": 1882227,
        "type_name": 'Blazers',
        "gender": 'Woman'
    },
    {
        "category_id": 1718088,
        "type_name": 'Waiskots',
        "gender": 'Woman'
    },
    {
        "category_id": 1882768,
        "type_name": 'Dresses',
        "gender": 'Woman'
    },
    {
        "category_id": 1882808,
        "type_name": 'Knitwear',
        "gender": 'Woman'
    },
    {
        "category_id": 1882926,
        "type_name": 'T-shirt',
        "gender": 'Woman'
    },
    {
        "category_id": 1718862,
        "type_name": 'Sweaters',
        "gender": 'Woman'
    },
    {
        "category_id": 1882891,
        "type_name": 'Jeans',
        "gender": 'Woman'
    },
    {
        "category_id": 1882845,
        "type_name": 'Trousers',
        "gender": 'Woman'
    },
    {
        "category_id": 1882988,
        "type_name": 'Shorts',
        "gender": 'Woman'
    },
    {
        "category_id": 1882899,
        "type_name": 'Skirt',
        "gender": 'Woman'
    },
    {
        "category_id": 1882792,
        "type_name": 'Shirts-tops',
        "gender": 'Woman'
    },
    {
        "category_id": 1719457,
        "type_name": 'Loungewear',
        "gender": 'Woman'
    },
    {
        "category_id": 1719408,
        "type_name": 'Suits',
        "gender": 'Woman'
    },
    {
        "category_id": 1719442,
        "type_name": 'Seamless',
        "gender": 'Woman'
    },
    {
        "category_id": 1718981,
        "type_name": 'Shoes',
        "gender": 'Woman'
    },
    {
        "category_id": 1719123,
        "type_name": 'Bags',
        "gender": 'Woman'
    },
    {
        "category_id": 1719379,
        "type_name": 'Accessories',
        "gender": 'Woman'
    },
    {
        "category_id": 1750767,
        "type_name": 'SpecialPrice',
        "gender": 'Woman'
    },
    {
        "category_id": 1719404,
        "type_name": 'Lingerie',
        "gender": 'Woman'
    },
    {
        "category_id": 1717639,
        "type_name": 'Jackets',
        "gender": 'Man'
    },
    {
        "category_id": 1717679,
        "type_name": 'Overshirts',
        "gender": 'Man'
    },
    {
        "category_id": 1717677,
        "type_name": 'Blazer',
        "gender": 'Man'
    },
    {
        "category_id": 1717658,
        "type_name": 'Waiskots',
        "gender": 'Man'
    },
    {
        "category_id": 1720409,
        "type_name": 'Loungewear',
        "gender": 'Man'
    },
    {
        "category_id": 1720315,
        "type_name": 'Shirts-tops',
        "gender": 'Man'
    },
    {
        "category_id": 1720373,
        "type_name": 'Maglietta',
        "gender": 'Man'
    },
    {
        "category_id": 1720387,
        "type_name": 'Polo',
        "gender": 'Man'
    },
    {
        "category_id": 1717716,
        "type_name": 'Sweaters',
        "gender": 'Man'
    },
    {
        "category_id": 1720321,
        "type_name": 'Sportswear',
        "gender": 'Man'
    },
    {
        "category_id": 1720273,
        "type_name": 'Jeans',
        "gender": 'Man'
    },
    {
        "category_id": 1720241,
        "type_name": 'Pantaloni',
        "gender": 'Man'
    },
    {
        "category_id": 1717689,
        "type_name": 'Dresses',
        "gender": 'Man'
    },
    {
        "category_id": 1720413,
        "type_name": 'Shoes',
        "gender": 'Man'
    },
    {
        "category_id": 1720458,
        "type_name": 'Bags',
        "gender": 'Man'
    },
    {
        "category_id": 1720640,
        "type_name": 'SpecialPrice',
        "gender": 'Man'
    }

]
