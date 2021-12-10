

import datetime
from bin.services.mapbox import MapBox
import logging
from bin.utils.statuses_enum import OrderSuccecedStatuses
from sqlalchemy.sql.expression import false, null
from bin.services.zara_new import Zara
from bin.models.clothes_bag_entity import ClotheInTheBag
from logging import exception
from bin.services.stripe import Stripe
from bin.services.database_new import Database
from bin.utils.data_classes import ClotheDataBag, ClotheLiked, CrediCard, Customer, Order, User, UserMMDScheleton
import json
import bin.utils.logger as logger
from flask import Response
import requests
_logger = logger.Logger()


class UsernameController:

    def __init__(self):
        pass

    def __build_clothe_in_the_bag_data(self, clothe,language, liked: bool = False, size:str=None):
        try:
            if clothe.brand.lower() == 'zara':
                clothe_info = Zara(language=language).get_clothe_poster(
                    id_clothe=clothe.id_clothe, user_liked=liked)
                if liked is False:
                    clothe_info['quantity'] = clothe.quantity
                if size is not None:
                    clothe_info['size'] = size
                return clothe_info
            else:
                return None
        except Exception as e:
            raise(e)

    def make_refund_money(self, order_id):
        try:
            logging.info(f'Executing refund money of order with id {order_id}')
            db = Database()
            stripe_client = Stripe()
            order = db.select_order(order_id=order_id)
            logging.info(f'Selected with success order data {order.__dict__}')
            for clothe in order.clothes:
                order_clothe_refund = Database().select_order(
                    order_id=clothe['id_order'])
                logging.info(f'Trying to make refund money with stripe of {order_clothe_refund}')
                if stripe_client().make_refund(order= order_clothe_refund) == 'succeeded':
                    logging.info(
                        f'Refund with success money width payment intent: {order_clothe_refund.stripe_id_intent}')
                else:
                    _logger.log('e', logger.LogLevel.error,
                                message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during making refund of money')
            return Response(self.__build_payload_response(message='An errore occured during making refund of money'), status=500, mimetype="application/json")

    def clothes_to_make_refund(self, id_user: int):
        try:
            logging.info(f'Selecting clothes on which user with id {id_user} can make refund')
            orders = Database().select_orders_delivered(id_user=id_user)
            clothes = []
            for order in orders:
                for clothe_dict in order.clothes:
                    if clothe_dict['returned'] == True:
                        clothe_dict['id_order'] = order.id
                        clothes.append(
                            clothe_dict
                        )
            logging.info(f'Selected with success clothe on which user can make refund: {clothes}')
            return Response(self.__build_payload_response(message='OK', payload=clothes), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during selecting clothe on which user can make refund.')
            return Response(self.__build_payload_response(message='An error occured during selecting clothe on which user can make refund'), status=500, mimetype="application/json")

    def clothes_inside_the_order(self, id_order):
        try:
            logging.info(f'Selecting clothes inside the order with id {id_order}')
            clothes = Database().select_clothes_inside_the_order(id_order=id_order)
            logging.info(f'Selected with succcess clothes inside the order: {clothes}')
            return Response(self.__build_payload_response(message='OK', payload=clothes), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting clothes inside the order.')
            return Response(self.__build_payload_response(message='An error occured while selecting clothes inside the order'), status=500, mimetype="application/json")

    def orders(self, id_user: int):
        try:
            logging.info(F'Selecting all orders of the user {id_user}')
            orders = Database().select_orders(id_user=id_user)
            procced_orders = []
            for order in orders:
                obj_dict = {}
                obj_dict['status'] = order.status_int
                obj_dict['id_order'] = order.id
                obj_dict['street_delivery'] = order.street_delivery
                obj_dict['city'] = order.city
                obj_dict['cap'] = order.zip_code
                obj_dict['day'] = str(order.start.strftime("%A")+'\n'+order.start.strftime("%d"))
                obj_dict['month'] = order.start.strftime("%B")
                obj_dict['date'] = order.start.strftime('%d/%m/%Y')
                obj_dict['end_time'] = order.end.strftime('%H:%M')
                obj_dict['courier_phone'] = '+39 3351539690' #TODO get this info from DB of couriers
                obj_dict['amount'] = float(order.amount)
                quantity = 0
                for clothe in order.clothes:
                    quantity += clothe['quantity']
                obj_dict['quantity'] = quantity
                procced_orders.append(obj_dict)
            orders_by_month = []
            months = []
            for order in procced_orders:
                if order['month'] not in months:
                    months.append(order['month'])
            for month in months:
                orders_by_month.append(
                    list(filter(lambda item: item['month'].lower() == month.lower(
                ), procced_orders))
                )
            
            logging.info(f'Selected with success orders of the user: {orders_by_month}')
            return Response(self.__build_payload_response(message='OK', payload=orders_by_month), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during while selecting orders of the user.')
            return Response(self.__build_payload_response(message='An error occured during while selecting orders of the user'), status=500, mimetype="application/json")

    def process_order(self, order: Order, type_return: bool = false):
        try:
            logging.info(f'Trying to proccessing order {order} with type_return {type_return}')
            db = Database()
            stripe_client = Stripe()
            logging.info('Trying to inser order inside DB with the status creating_payment_intent')
            order_id = db.insert_order(
                order=order, status=OrderSuccecedStatuses.creating_payment_intent.value)
            logging.info('Inserted with success order inside the DB')
            logging.info(f'Trying to select credit card id on stripe with id {order.credit_card_id}')
            card_id_stripe = db.select_card(
                id_card=order.credit_card_id)
            logging.info(f'Selected with success credit card id stripe')
            logging.info(f'Selecting user data with id {order.id_user}')
            user = db.select_user(id_user=order.id_user)
            logging.info(f'Selected with success user data')
            logging.info(f'Trying to create payment intent on stripe')
            payment_intent_id = stripe_client.create_payment_intent(
                email=user.email, id_card=card_id_stripe, amount=order.amount, id_customer=user.customer_id)
            logging.info(f'Created with success payment intent with id {payment_intent_id}')
            logging.info(f'Trying to confirm payment intent')
            if stripe_client.confirm_payment_intent(id=payment_intent_id) == 'succeeded':
                logging.info(f'Confirmed with success payment intent with id {payment_intent_id}')
                response_db = db.update_status_order(
                    id_order=order_id, status=OrderSuccecedStatuses.searching_for_the_courier.value, payment_intent_id=payment_intent_id)
                logging.info(f'Updated status of order with success {response_db}')
                response_db = db.delete_clothes_from_the_bag(
                    id_user=order.id_user)
                logging.info(f'Removed clothes from the bag')
                #TODO Continue logic
                self.__calculate_times_to_take_and_prepare_order(order=order, order_id=order_id)
                if type_return:
                    logging.info(f'Changing status of clothes on which user will do refund inside the order with id {order_id}')
                    for clothe in order.clothes_dict:
                        db.change_status_returned_clothe_inside_order(
                            order_id=order_id, clothe_id=clothe['id'])
                # TODO test this logic
                logging.info('Making request to API COURIER to find couriers')
                #res = requests.get(
                #    f'http://localhost:8081/api_v1/courier/search_courier/{order_id}')
                return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")
            else:
                response_db = db.update_status_order(
                    id_order=order_id, status=OrderSuccecedStatuses.confirmationf_payment_intent_failed.value)
                return Response(self.__build_payload_response(message='FAILED CONFIRMATION OF PAYMENT'), status=500, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while processing order')
            return Response(self.__build_payload_response(message='An error occured while processing order'), status=500, mimetype="application/json")

    def add_quantity_to_the_clothe(self, id_user: int, id_clothe: str):
        try:
            logging.info(f'Adding quantity to the clothe of user with id {id_user} and clothe id {id_clothe}')
            response_db = Database().add_quantity_clothe(
                id_user=id_user, id_clothe=id_clothe)
            logging.info(f'Added with success quantity {response_db}')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while tried to add quantity to he clothe ')
            return Response(self.__build_payload_response(message='An error occured while tried to add quantity to he clothe'), status=500, mimetype="application/json")

    def remove_quantity_to_the_clothe(self, id_user: int, id_clothe: str):
        try:
            logging.info(f'Removing quantity from the clothe')
            response_db = Database().remove_quantity_clothe(
                id_user=id_user, id_clothe=id_clothe)
            logging.info(F'Updated with success quantity of clothe of user {id_user} and id_clothe {id_clothe}')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while removing quantity of the clothe')
            return Response(self.__build_payload_response(message='An error occured while removing quantity of the clothe'), status=500, mimetype="application/json")

    def liked_clothes(self, id_user: int, language:str):
        try:
            logging.info(f'Selecting liked clothes of user with id {id_user}')
            clothes = Database().select_liked_clothes(id_user=id_user)
            clothes_procceded = []
            logging.info(F'Selected with success clothes from db {clothes}')
            if isinstance(clothes, list):
                for clothe in clothes:
                    clothes_procceded.append(
                        self.__build_clothe_in_the_bag_data(clothe=clothe, liked=True, language=language))
            else:
                clothes_procceded.append(
                    self.__build_clothe_in_the_bag_data(clothe=clothes, liked=True, language=language))
            logging.info(f'Selected with success clothes liked {clothes_procceded}')
            return Response(self.__build_payload_response(message='OK', payload=clothes_procceded), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while adding clothe liked')
            return Response(self.__build_payload_response(message='An error occured while adding clothe liked'), status=500, mimetype="application/json")

    def bag_select_clothes(self, id_user: int, language:str):
        try:
            logging.info(f'Selecting clothes inside the bag of the user with id {id_user}')
            clothes = Database().select_clothes_in_the_bag(id_user=id_user)
            print(clothes)
            clothes_procceded = []
            if isinstance(clothes, list):
                for clothe in clothes:
                    clothes_procceded.append(
                        self.__build_clothe_in_the_bag_data(clothe=clothe, size=clothe.size, language=language))
            else:
                clothes_procceded.append(
                    self.__build_clothe_in_the_bag_data(clothe=clothes, size=clothes.size, language=language))
            logging.info(f'Selected with success clothes inside the bag {clothes_procceded}')
            return Response(self.__build_payload_response(message='OK', payload=clothes_procceded), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecting clothes inside the bag.')
            return Response(self.__build_payload_response(message='An error occured while selecting clothes inside the bag'), status=500, mimetype="application/json")

    def remove_clothe_from_the_bag(self, id_clothe: str, id_user: int):
        try:
            logging.info(f'Removing clothe inside')
            response_db = Database().delete_clothe_from_the_bag(
                id_clothe=id_clothe, id_user=id_user)
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while removing clothe from the bag.')
            return Response(self.__build_payload_response(message='An error occured while removing clothe from the bag'), status=500, mimetype="application/json")

    def add_clothe_inside_the_bag(self, clothe: ClotheDataBag):
        try:
            logging.info(F'Adding clothe inside the bag of the user with id {clothe.id_user}')
            response_db = Database().insert_clothe_inside_the_bag(clothe=clothe)
            logging.info(f'Inserted with success clothe inside the bag {response_db}')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while adding clothe inside the bag')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def dislike_clothe(self, id_clothe: str, id_user: int):
        try:
            logging.info(f'Removing liked clothe with id {id_user} of the user {id_clothe}')
            response_db = Database().remove_liked_clothe(
                id_clothe=id_clothe, id_user=id_user)
            logging.info(f'Removed with success clothe liked {response_db}')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while removing liked clothe.')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def like_clothe(self, clothe: ClotheLiked):
        try:
            logging.info(f'Adding clothe liked {clothe}')
            response_db = Database().insert_liked_clothe(clothe=clothe)
            logging.info(f'Added with success clothe liked {response_db}')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while adding liked clothe')
            return Response(self.__build_payload_response(message='An error occured while adding liked clothe'), status=500, mimetype="application/json")

    def register(self, user: Customer):
        try:
            logging.info('Checking if the user with the same data already exist')
            user_ent = Database().select_user()
            logging.info(f'Selected with success user data {user_ent}')
            if user_ent is not None:
                logging.info(f'User already exist')
                return Response(self.__build_payload_response(message='Register FAILED'), status=404, mimetype="application/json")
            else:
                logging.info(f'Executing register of the user')
                stripe_client = Stripe()
                logging.info(f'Creating stripe customer')
                user.customer_id = stripe_client.create_stripe_customer(
                    user=user)
                logging.info('Created with success customr on stripe')
                logging.info(f'Inserting user data inside the DB')
                user_ent = Database().insert_new_user(user=user)
                logging.info(f'Adding credit card to in the stripe')
                user.credit_card.id_stripe = stripe_client.add_new_credit_card(
                    user=user_ent, card=user.credit_card)
                logging.info(f'Created with success credit card on stripe')
                logging.info(f'Coonecting credit card {user.credit_card.id_stripe} to the user {user.customer_id}')
                stripe_client.connect_card_to_user(
                    user_id_stripe=user.customer_id, credit_card_id_stripe=user.credit_card.id_stripe)
                logging.info(f'Inserting credit card inside the database')
                user.credit_card.id = Database().insert_card(
                    id_user=user_ent.id, card=user.credit_card)
                logging.info(f'Inserted with success credit card inside the DB')
                return Response(self.__build_payload_response(message='OK', payload={'user_id': user_ent.id}), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while executing registration of the user.')
            return Response(self.__build_payload_response(message='An error occured while executing registration of the user.'), status=500, mimetype="application/json")

    def login(self, user_data_login: User):
        try:
            logging.info('Selecting user data from the database')
            user = Database().select_user_id(user=user_data_login)
            if user is None:
                logging.info('User doenst exist inside the DB')
                return Response(self.__build_payload_response(message='LOGIN FAILED'), status=404, mimetype="application/json")
            else:
                logging.info(f'Executed with success login of the user')
                return Response(self.__build_payload_response(message='OK', payload={'user_id': user.id}), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while executing loging')
            return Response(self.__build_payload_response(message='An error occured while executing loging'), status=500, mimetype="application/json")

    def remove_card(self, id_card: int, id_user: int):
        try:
            logging.info(f'Removing credit card with id {id_card} of the user {id_user}')
            response_db = Database().delete_card(id_user=id_user, id_card=id_card)
            logging.info('Removed with success credit card')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while removing credit card')
            return Response(self.__build_payload_response(message='An errore occured while removing credit card'), status=500, mimetype="application/json")

    def new_user_card(self, card: CrediCard, id_user: int):
        try:
            logging.info('Selecting user credit card')
            user = Database().select_user(id_user=id_user)
            card.card_number = card.card_number.replace(' ', '')
            stripe_client = Stripe()
            logging.info('Adding new credit card on stripe')
            card.id_stripe = stripe_client.add_new_credit_card(
                user=user, card=card)
            logging.info(f'Connectinc credit card with id {card.id_stripe} of the user {id_user}')
            stripe_client.connect_card_to_user(
                user_id_stripe=user.customer_id, credit_card_id_stripe=card.id_stripe)
            logging.info('Inserting credit card inside the DB')
            card.id = Database().insert_card(id_user=id_user, card=card)
            response_dict = {
                "last_num": card.card_number[-4:], 'id_card': card.id, 'card_type': card.card_type}

            return Response(self.__build_payload_response(message='OK', payload=response_dict), status=200, mimetype="application/json")

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while adding new user card')
            return Response(self.__build_payload_response(message='An error occured while adding new user card'), status=500, mimetype="application/json")

    def user_main_info(self, id_user: int):
        try:
            logging.info('Selecting user info from the DB')
            user = Database().select_user(id_user=id_user)
            user_dict = {}
            user_dict['name'] = user.name
            user_dict['surname'] = user.surname
            user_dict['phone_number'] = user.phone_number
            user_dict['residence'] = user.residence
            user_dict['city'] = user.city
            user_dict['zip_code'] = user.zip_code
            logging.info(f'Selected with succes main info of the user {user_dict}')
            return Response(self.__build_payload_response(message='OK', payload=user_dict), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecing main info of the user')
            return Response(self.__build_payload_response(message='An error occured while selecing main info of the user'), status=500, mimetype="application/json")

    def user_cards(self, id_user: int):
        try:
            logging.info(f'Selecting credit cards of the user with id {id_user}')
            cards_entity = Database().select_cards(id_user=id_user)
            cards = []
            for card in cards_entity:
                cards.append(
                    {"last_num": card.card_number[-4:], 'id_card': card.id, 'card_type': card.card_type})
            logging.info(F'Selected with success credit cards {cards}')
            return Response(self.__build_payload_response(message='OK', payload=cards), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while selecing user credit cards.')
            return Response(self.__build_payload_response(message='An errore occured during loggin'), status=500, mimetype="application/json")

    def modify_user_main_info(self, user: UserMMDScheleton):
        try:
            db = Database()
            logging.info(f'Updating user main info {user}')
            response_update = db.update_main_info(user=user)
            logging.info(f'Updated with success main info of user')
            return Response(self.__build_payload_response(message='OK'), status=200, mimetype="application/json")
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while modifing user main info ')
            return Response(self.__build_payload_response(message='An error occured while modifing user main info'), status=500, mimetype="application/json")

    def __build_payload_response(self, message: str, payload=None) -> dict:
        return json.dumps({
            "message": message,
            "payload": payload
        })
    
    def __calculate_times_to_take_and_prepare_order(self, order:Order, order_id):
        try:
            logging.info(f'Trying to calculate times on which order have to be prepared and delivered')
            final_list_duration = []
            logging.info(f'Trying to set end time of delivery based on {order.day_delivery }{order.hour_delivery}...')
            end = datetime.datetime.strptime(order.day_delivery +'T' + order.hour_delivery, "%Y-%m-%dT%H:%M%p")
            logging.info(f'End time of delivery is {end}')
            start = end
            for index, shop in reversed(list(enumerate(order.directions))):
                print(index)
                if index == len(order.directions)-1:
                    
                    lat_user_pos, lng_user_pos = MapBox().get_lat_lng_of_position(street_name=order.street_delivery, country='Italia', city= order.city)
                    logging.info(f'Get position lat lng of user {lat_user_pos} {lng_user_pos}')
                    duration_date_time = MapBox().caluclate_duration_between_2_positions(lat1=lat_user_pos,lng1= lng_user_pos, lat2=shop['lat'], lng2=shop['lng'])
                    logging.info(f'Get duration date time of 2 positions {duration_date_time}')
                    logging.info(f'Trying to make difference between start time end another time on which user shoul be at the shop...')
                    start = start - datetime.timedelta(hours= duration_date_time.hour, minutes= duration_date_time.minute, seconds=duration_date_time.second)
                    logging.info(f'Time on which user must be on the shop is {start}')
                    logging.info(F'Trying to select shop info by id{shop} ')
                    shop_entity_obj = Database().select_shop_by_id(id_shop=shop['id_shop'])
                    logging.info(f'Selected with success shop info from db {shop_entity_obj}')
                    
                    shop_clothes_list = []
                    for clothe_id in shop['clothes_ids']:
                        filtered_clothe = list(filter(lambda item: str(item['id']) == clothe_id, order.clothes_dict))
                        shop_clothes_list.append(filtered_clothe[0])
                    logging.info(f'Builded list of clothes for shop {shop_clothes_list}')
                    final_list_duration.append({
                        "shop_id":shop['id_shop'],
                        "clothes":shop_clothes_list,
                        "street":f'{shop_entity_obj.street} {shop_entity_obj.city} {shop_entity_obj.zip_code}',
                        "brand":shop_entity_obj.brand,
                        "estimatedTimeArrives":start.isoformat()
                    })
                    logging.info('Trying to insert order inside the shop Row...')
                    start = start - datetime.timedelta(hours=0, minutes=20, seconds=0)
                    Database().insert_order_shop(id_order= order_id, id_shop= shop['id_shop'], prepare_to= start, clothes=shop_clothes_list)
                else:
                    duration_date_time = MapBox().caluclate_duration_between_2_positions(lat1=order.directions[index+1]['lat'],lng1= order.directions[index+1]['lng'], lat2=shop['lat'], lng2=shop['lng'])
                    logging.info(f'Get duration date time of 2 positions {duration_date_time}')
                    start = start - datetime.timedelta(hours= duration_date_time.hours, minutes= duration_date_time.minutes, seconds=duration_date_time.seconds)
                    logging.info(f'Time on which user must be on the shop is {start}')
                    logging.info(F'Trying to select shop info by id {shop["id_shop"]}')
                    shop_entity_obj = Database().select_shop_by_id(id_shop=shop['id_shop'])
                    logging.info(f'Selected with success shop info from db {shop_entity_obj}')

                    shop_clothes_list = []
                    for clothe_id in shop['clothes_ids']:
                        filtered_clothe = list(filter(lambda item: str(item['id']) == clothe_id, order.clothes_dict))
                        shop_clothes_list.append(filtered_clothe[0])
                    logging.info(f'Builded list of clothes for shop {shop_clothes_list}')
                        
                    final_list_duration.append({
                        "shop_id":shop['id_shop'],
                        "clothes":shop_clothes_list,
                        "street":f'{shop_entity_obj.street} {shop_entity_obj.city} {shop_entity_obj.zip_code}',
                        "brand":shop_entity_obj.brand,
                        "estimatedTimeArrives":start.isoformat()
                    })
                    logging.info('Trying to insert order inside the shop Row...')
                    start = start - datetime.timedelta(hours=0, minutes=20, seconds=0)
                    Database().insert_order_shop(id_order= order_id, id_shop= shop['id'], prepare_to= start, clothes=shop_clothes_list)
            
            logging.info(f'Updating start time of order {order_id} inside DB {start}')
            Database().update_start_time_order(id= order_id, start= start)
            logging.info(f'Updating directions dict of order {order_id} inside DB {final_list_duration}')
            Database().update_directions(id= order_id, directions= final_list_duration)
            return True    
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured while calculating time on which order have to be prepared.')
            raise(e)
    
    def test_order_procced(self):
        try:
            order= Order(
                amount= 10,
                id_user=17,
                hour_delivery='13:50AM',
                day_delivery='2021-02-13',
                street_delivery= 'via Amerigo Vespucci 18',
                credit_card_id=1,
                clothes_dict=[{
                    'id': 116382347,
                    'quantity': 1,
                    'size': 'S',
                    'brand': 'Zara',
                    'cost': '12',
                    'firstImage': 'bho',
                    'title': 'Test',
                    'returned': False
                },{
                    'id': 116136005,
                    'quantity': 1,
                    'size': 'S',
                    'brand': 'Zara',
                    'cost': '12',
                    'firstImage': 'bho',
                    'title': 'Test',
                    'returned': False
                }],
                city='Cormano',
                zip_code=20032,
                directions=json.loads('[{"id_shop": 3307, "lat": 9.18795235, "lng": 45.46365356, "clothes_ids": ["116382347", "116136005"]}]')
            )
            logging.info(order)
            self.__calculate_times_to_take_and_prepare_order(order=order, order_id=69)
            #STEP 1 => Calculate direction from initial point to shops and to user specifing the time on which courier must be at the user house
        except Exception as e:
            logging.error(f'Erorr {e}')
