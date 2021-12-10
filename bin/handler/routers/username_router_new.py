from bin.services.mapbox import MapBox
from sqlalchemy.sql.expression import true
from bin.controller.user_controller_new import UsernameController
from flask import Flask, request, Response
import datetime
import json
from bin.utils.data_classes import Customer, CrediCard, User, ClotheLiked, Order, ClotheDataBag, UserMMDScheleton
import logging


class UsernameRouter:
    def __init__(self, app):
        self.app = app
        
        @app.route('/api_v1/dir', methods=['GET'])
        def s():
            shops_lat_lng = [
                {
                    "lat": "9.1858432",
                    "lng": "45.4723719",
                },
                {
                    "lat": "9.1770885",
                    "lng": "45.4723719",
                },
                {
                    "lat": "9.2216775",
                    "lng": "45.4660216",
                }
            ]
            response = MapBox().calculate_directions(lat_lng_list=shops_lat_lng)
            return "I'm alive!"
        
        
        

        @app.route('/api_v1/user/register', methods=['POST'])
        def register():
            try:
                request_json = request.get_json()
                logging.info(
                    f'Request body received: {request_json} => /api_v1/user/register')

                customer = Customer.Schema().loads(
                    json.dumps(request_json['payload']))
                logging.info(
                    F'Created with success customer object: {customer}')
                return UsernameController().register(user=customer)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/register: {e}')

        @app.route('/api_v1/user/login', methods=['POST'])
        def login():
            try:
                request_json = request.get_json()
                user = User.Schema().loads(json.dumps(request_json['payload']))
                logging.info(
                    f'Request body received: {user} => /api_v1/user/login')
                return UsernameController().login(user_data_login=user)
            except Exception as e:
                logging.error(f'An errore occured /api_v1/user/login: {e}')

        @app.route('/api_v1/user/like_clothe', methods=['POST'])
        def like_clothe():
            try:
                request_json = request.get_json()
                clothe = ClotheLiked.Schema().loads(
                    json.dumps(request_json['payload']))
                logging.info(
                    f'Request body received: {clothe} => /api_v1/user/like_clothe')
                return UsernameController().like_clothe(clothe=clothe)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/like_clothe: {e}')

        @app.route('/api_v1/user/dislike_clothe/<id_clothe>/<id_user>', methods=['DELETE'])
        def dislike_clothe(id_clothe, id_user):
            try:
                logging.info(
                    f'Received user id :{id_user} and clothe id {id_clothe} => /api_v1/user/dislike_clothe')
                return UsernameController().dislike_clothe(id_clothe=id_clothe, id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/dislike_clothe/<id_clothe>/<id_user>: {e}')

        @app.route('/api_v1/user/add_clothe_to_the_bag', methods=['POST'])
        def add_clothe_to_the_bag():
            try:
                clothe = ClotheDataBag.Schema().loads(
                    json.dumps(request.get_json()['payload']))
                logging.info(
                    f'Object received {clothe} => /api_v1/user/add_clothe_to_the_bag')
                return UsernameController().add_clothe_inside_the_bag(clothe=clothe)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/add_clothe_to_the_bag: {e}')

        @app.route('/api_v1/user/remove_clothe_from_the_bag/<id_clothe>/<id_user>', methods=['DELETE'])
        def remove_clothe_from_the_bag(id_clothe, id_user):
            try:
                logging.info(
                    f'Received {id_clothe} and {id_user} => /api_v1/user/remove_clothe_from_the_bag')
                return UsernameController().remove_clothe_from_the_bag(id_clothe=id_clothe, id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/remove_clothe_from_the_bag/<id_clothe>/<id_user>: {e}')

        @app.route('/api_v1/user/<id_user>/clothes_in_the_bag/<language>', methods=['GET'])
        def clothes_in_the_bag(id_user, language):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/clothes_in_the_bag')
                return UsernameController().bag_select_clothes(id_user=id_user, language=language)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/clothes_in_the_bag: {e}')

        @app.route('/api_v1/user/<id_user>/liked_clothes/<language>', methods=['GET'])
        def liked_clothes(id_user,language):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/liked_clothe')
                return UsernameController().liked_clothes(id_user=id_user, language=language)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/liked_clothes: {e}')

        @app.route('/api_v1/user/<id_user>/add_quantity/<id_clothe>', methods=['PUT'])
        def add_quantity(id_user, id_clothe):
            try:
                logging.info(
                    f'Received {id_user} and {id_clothe} => /api_v1/user/<id_user>/add_quantity/<id_clothe>')
                return UsernameController().add_quantity_to_the_clothe(id_user=id_user, id_clothe=id_clothe)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/add_quantity/<id_clothe>: {e}')

        @app.route('/api_v1/user/<id_user>/remove_quantity/<id_clothe>', methods=['PUT'])
        def remove_quantity(id_user, id_clothe):
            try:
                logging.info(
                    f'Received {id_user} and {id_clothe} => /api_v1/user/<id_user>/remove_quantity/<id_clothe>')
                return UsernameController().remove_quantity_to_the_clothe(id_user=id_user, id_clothe=id_clothe)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/remove_quantity/<id_clothe>: {e}')

        @app.route('/api_v1/user/procced_order', methods=['POST'])
        def process_order():
            try:
                request_json = request.get_json()['payload']
                request_json['directions'] = json.loads(request_json['directions'])
                order = Order.Schema().loads(
                    json.dumps(request.get_json()['payload']))
                logging.info(
                    f'Object request : {order} => /api_v1/user/procced_order')
                return UsernameController().process_order(order=order)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/procced_order: {e}')

        @app.route('/api_v1/user/<id_user>/add_new_card', methods=['POST'])
        def add_new_card(id_user):
            try:
                card = CrediCard.Schema().loads(json.dumps(
                    request.get_json()['payload']['credit_card']))
                logging.info(
                    f'Object request : {card} => /api_v1/user/<id_user>/add_new_card')
                return UsernameController().new_user_card(card=card, id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/add_new_card: {e}')

        @app.route('/api_v1/user/<id_user>/remove_card/<id_card>', methods=['DELETE'])
        def remove_card(id_user, id_card):
            try:
                logging.info(
                    f'Received {id_user} and {id_card} => /api_v1/user/<id_user>/remove_card/<id_card>')
                return UsernameController().remove_card(id_card=id_card, id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/remove_card/<id_card>: {e}')

        @app.route('/api_v1/user/<id_user>/get_info', methods=['GET'])
        def get_info_user(id_user):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/get_info')
                return UsernameController().user_main_info(id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/get_info: {e}')

        @app.route('/api_v1/user/<id_user>/modify_main_info_user', methods=['PUT'])
        def modify_main_info_user(id_user):
            try:
                print(request.get_json()['payload'])
                user = UserMMDScheleton.Schema().loads(json.dumps(
                    request.get_json()['payload']))
                logging.info(
                    f'Object request : {user} => /api_v1/user/<id_user>/modify_main_info_user')
                return UsernameController().modify_user_main_info(user=user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/modify_main_info_user: {e}')

        @app.route('/api_v1/user/<id_user>/get_cards', methods=['GET'])
        def get_cards_user(id_user):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/get_cards')
                return UsernameController().user_cards(id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/get_cards: {e}')

        @app.route('/api_v1/user/<id_user>/get_orders', methods=['GET'])
        def get_orders(id_user):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/get_orders')
                return UsernameController().orders(id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/get_orders: {e}')

        @app.route('/api_v1/user/<id_order>/get_clothes_order', methods=['GET'])
        def get_clothes_order(id_order):
            try:
                logging.info(
                    f'Received {id_order} => /api_v1/user/<id_order>/get_clothes_order')
                return UsernameController().clothes_inside_the_order(id_order=id_order)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_order>/get_clothes_order: {e}')

        @app.route('/api_v1/user/<id_user>/get_clothes_to_return', methods=['GET'])
        def get_clothes_to_return(id_user):
            try:
                logging.info(
                    f'Received {id_user} => /api_v1/user/<id_user>/get_clothes_to_return')
                return UsernameController().clothes_to_make_refund(id_user=id_user)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/<id_user>/get_clothes_to_return: {e}')

        @app.route('/api_v1/user/procced_order_return', methods=['POST'])
        def process_order_return():
            try:

                order = Order.Schema().loads(
                    json.dumps(request.get_json()['payload']))
                logging.info(
                    f'Object request : {order} => /api_v1/user/procced_order_return')
                return UsernameController().process_order(order=order, type_return=true)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/procced_order_return: {e}')

        @app.route('/api_v1/user/make_refund/<order_id>', methods=['POST'])
        def make_refund(order_id):
            try:
                logging.info(
                    f'Received {order_id} => /api_v1/user/make_refund/<order_id>')
                return UsernameController().make_refund_money(order_id=order_id)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/make_refund/<order_id>: {e}')
                # TODO Finish this endpoint

        @app.route('/api_v1/user/get_hour_initial_delivery', methods=['POST'])
        def get_hour_initial_delivery():
            """Get home page posters info from DB."""
            username_controller = UsernameController()
            time_start_delivery = datetime.datetime.now()
            print(time_start_delivery.strftime('%x'))

            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": {
                            "hour_start": int(time_start_delivery.hour),
                            "minutes_start": int(time_start_delivery.minute),
                            "date": time_start_delivery.strftime('%x')
                        }
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        @app.route('/api_v1/user/test/order_procced', methods=['GET'])
        def test_order_procced():
            try:
                UsernameController().test_order_procced()
                return Response(200)
            except Exception as e:
                logging.error(
                    f'An errore occured /api_v1/user/make_refund/<order_id>: {e}')
