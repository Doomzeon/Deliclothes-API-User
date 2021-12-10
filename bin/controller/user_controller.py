from flask import Response
import logging
from bin.services.authentication import Jwt
from bin.services.zara_new import Zara
import json
import datetime
from itertools import permutations
from bin.services.payments import StripePayment
from bin.utils.data_classes import Customer, CrediCard, User, ClotheDataBag, Order, ClotheLiked, UserInfo
from bin.utils.database import Database
import bin.utils.logger as logger  # import LogLevel, Logger
import requests

_logger = logger.Logger()


class UsernameController:

    def __init__(self, username: str = None):
        self._username = username

    def test_hour_delivery(self, orders: list) -> Response:
        try:
            # TODO => determine in some way which service to use in base of brand to calculate hour of delivery
            orders_dict = []
            for order in orders:
                refer_id = self.__splite_size_code(
                    order['size_selected'])  # TODO change it?
                print(f'Refererence id of clothe is {refer_id}')
                shop_list = Zara().get_product_availability(
                    refer_id=refer_id, lat='45.4642035', lng='9.189982')
                orders_dict.append(shop_list)

            print(orders_dict)
            print('Processing delivery directions')
            directions = Zara().directions_delivery(orders_dict)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": directions  # json.dumps(directions)
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            print(e)
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "OK",
                        "payload": "json.dumps(directions)"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def __splite_size_code(self, order_size: dict) -> str:
        try:
            splitted_size = order_size.split('-')
            # lat= lng= 9.189982
            return splitted_size[0][:-2]
        except Exception as e:
            print(e)

    def modify_name(self, id_user, name: str):
        try:
            cards_entity = Database().modify_name(id_user, name)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK"
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def modify_surname(self, id_user, surname: str):
        try:
            cards_entity = Database().modify_surname(id_user, surname)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK"
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def modify_residence(self, id_user, residence: str):
        try:
            cards_entity = Database().modify_residence(id_user, residence)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK"
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def modify_phone(self, id_user, phone: str):
        try:
            cards_entity = Database().modify_phone(id_user, int(phone))
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK"
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_user_cards(self, id_user: int):
        try:
            cards_entity = Database().get_cards_user(id_user)
            cards_list = []
            for card in cards_entity:
                cards_list.append(
                    {
                        'last_num': card.card_number[-4:],
                        'id_card': card.id,
                        'card_type': card.card_type
                    }
                )
            print(cards_list)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": cards_list
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_user_info(self, id_user: int):
        try:
            user_entity = Database().get_info_user(id_user)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": {
                            'name': user_entity.name,
                            'surname': user_entity.surname,
                            'phone_number': str(user_entity.phone_number),
                            'residence': user_entity.residence,
                            'city': user_entity.city,
                            'zip_code': user_entity.zip_code
                        }
                    }),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def add_new_card(self, card: CrediCard, id_user):
        try:
            db = Database()
            user = db.select_user(id_user)
            customer = Customer(email=user.email, name=user.name,
                                id=id_user,
                                customer_id=user.customer_id,
                                surname=user.surname,
                                residence=user.residence,
                                id_city=user.id_city,
                                phone_number=user.phone_number,
                                country_code=user.country_code,
                                language=user.language,
                                credit_card=card)
            customer.credit_card.card_number = customer.credit_card.card_number.replace(
                ' ', '')
            customer.credit_card.id_stripe = StripePayment().create_credit_card(
                customer=customer)
            StripePayment().add_credit_card_to_customer(customer=customer)
            customer.credit_card.id = db.insert_new_credit_card(
                customer=customer)
            print(customer.credit_card.id)
            return Response(
                json.dumps(
                    {
                        "status": 201,
                        "message": "OK",
                        "payload": {
                            'last_num': customer.credit_card.card_number[-4:],
                            'id_card': customer.credit_card.id,
                            'card_type': customer.credit_card.card_type
                        }
                    }
                ),
                status=201,
                mimetype="application/json"
            )

        except Exception as e:
            print(e)
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def remove_card(self, id_card, id_user):
        try:
            if Database().remove_card(id_user, id_card):
                return Response(
                    json.dumps(
                        {
                            "status": 200,
                            "message": "OK"
                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 500,
                            "message": "Internal server error."
                        }
                    ),
                    status=500,
                    mimetype="application/json"
                )
        except Exception as e:
            print(e)
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def login_user(self, user: User):
        try:
            db = Database()
            logging.info(f'\nSearching for the user inside Database.')
            user_entity = db.select_user_data_login(user=user)

            logging.info(
                f'\nValidating if user exist. User data: {user_entity}')
            if user_entity is None:
                return Response(
                    json.dumps(
                        {
                            "status": 404,
                            "message": "Email provided or password is wrong"
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )
            logging.info(f'\nSelected with success user data {user_entity}')

            #jwt_token = Jwt().encode_auth_token(customer)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": {
                            'user_id': user_entity.id
                        }
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during login.')

    def register_account_data(self, customer: Customer) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            db = Database()

            logging.info(f'\nVerifying if user with email passed exists')
            if db.select_user_data(customer=customer) is not None:
                return Response(
                    json.dumps(
                        {
                            "status": 404,
                            "message": "User with this email already exist"
                        }
                    ),
                    status=404,
                    mimetype="application/json"
                )

            payments = StripePayment()

            logging.info(f'\nCreating new customer on Stripe.')
            customer.customer_id = payments.create_stripe_customer(
                customer=customer)
            logging.info(f'\nCustomer id on stripe is {customer.customer_id}')

            logging.info(f'\nAdding customer inside the Database.')
            customer.id = db.insert_new_user(customer=customer)
            logging.info(f'\nUser id inserted is {customer.id}')

            logging.info(f'\nCreating new credit card on Stripe.')
            customer.credit_card.card_number = customer.credit_card.card_number.replace(
                ' ', '')
            customer.credit_card.id_stripe = payments.create_credit_card(
                customer=customer)
            logging.info(
                f'\Credit card id on stripe is {customer.credit_card.id_stripe}')

            logging.info(f'Adding credit card to the customer on stripe')
            payments.add_credit_card_to_customer(customer=customer)

            logging.info(f'\nAdding credit card inside the Database.')
            db.insert_new_credit_card(customer=customer)
            logging.info(f'\nAdded with success credit card entity')

            logging.info(f'\nCustomer info : {customer}')
            jwt_token = Jwt().encode_auth_token(customer)
            return Response(
                json.dumps(
                    {
                        "status": 201,
                        "message": "OK",
                        "payload": {
                            'jwt': str(jwt_token),
                            'user_data': Customer.Schema().dump(customer)
                        }
                    }
                ),
                status=201,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An error occured during registration of a new user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def like_clothe(self, clothe_liked: ClotheLiked):
        try:
            db = Database()
            logging.info('Tying to insert clothe liked inside DB')
            if db.like_clothe(clothe_liked=clothe_liked):
                return Response(
                    json.dumps(
                        {
                            "status": 200,
                            "message": "OK"
                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 400,
                            "message": "Something is wrong"
                        }
                    ),
                    status=400,
                    mimetype="application/json"
                )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding clothe liked inside the Database.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def dislike_clothe(self, id_clothe: str, id_user: int) -> Response:
        try:
            db = Database()
            if db.dislike_clothe(id_clothe=id_clothe, id_user=id_user):
                return Response(
                    json.dumps(
                        {
                            "status": 200,
                            "message": "OK"
                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 400,
                            "message": "Something is wrong"
                        }
                    ),
                    status=400,
                    mimetype="application/json"
                )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while removing clothe liked from the DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def add_clothe_to_the_bag(self, clothe_data_bag: ClotheDataBag) -> Response:
        try:
            db = Database()
            if db.add_clothe_to_the_bag(clothe_data_bag=clothe_data_bag):
                return Response(
                    json.dumps(
                        {
                            "status": 201,
                            "message": "OK"
                        }
                    ),
                    status=201,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 400,
                            "message": "Something is wrong"
                        }
                    ),
                    status=400,
                    mimetype="application/json"
                )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while add clothe to the bag.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def remove_clothe_from_the_bag(self, id_clothe: str, id_user: int) -> Response:
        try:
            db = Database()
            if db.remove_clothe_from_the_bag(id_clothe=id_clothe, id_user=id_user):
                return Response(
                    json.dumps(
                        {
                            "status": 202,
                            "message": "OK"
                        }
                    ),
                    status=202,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 400,
                            "message": "Something is wrong"
                        }
                    ),
                    status=400,
                    mimetype="application/json"
                )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while add to DB clothe liked.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def select_clothes_in_the_bag(self, id_user: int) -> Response:
        try:
            db = Database()
            clothes_in_the_bag_info = db.select_clothes_in_the_bag(
                id_user=id_user)
            logging.info(
                f'Selected with success clothes inside the bag {clothes_in_the_bag_info}')
            clothes_proccessed = []
            if isinstance(clothes_in_the_bag_info, list):
                for clothe in clothes_in_the_bag_info:
                    product_info = Zara().get_product_info_data(
                        clothe.id_clothe)
                    product_info['quantity'] = clothe.quantity
                    clothes_proccessed.append({
                        'clothe_info_db': ClotheDataBag.Schema().dump(clothe),
                        'clothe_info': product_info})
            else:
                product_info = Zara().get_product_info_data(
                    clothe.id_clothe)
                product_info['quantity'] = clothes_in_the_bag_info.quantity
                clothes_proccessed.append({
                    'clothe_info_db': ClotheDataBag.Schema().dump(clothes_in_the_bag_info),
                    'clothe_info': product_info})

            logging.info(
                f'Proccessed with success clothe inside the bag {clothes_proccessed}')
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "Selected with success clothes",
                        "payload": json.dumps(clothes_proccessed)
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while selecting clothes inside the bag of the user.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def select_liked_clothes(self, id_user: int) -> Response:
        try:
            db = Database()
            clothes_liked = db.select_liked_clothes(id_user=id_user)
            logging.info(
                f'Selected with success clothes liked of the user {id_user}. Clothes: {clothes_liked}')
            clothes_proccessed = []
            if isinstance(clothes_liked, list):
                for clothe in clothes_liked:
                    clothes_proccessed.append(
                        Zara(language='en').get_clothes(clothe.id_clothe, True))
            else:
                clothes_proccessed.append(
                    Zara().get_product_info_data(clothes_liked.id_clothe, True))

            logging.info(
                f'Procced with success clothes liekd by user : {clothes_proccessed}')
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "Selected with success clothes",
                        "payload": json.dumps(clothes_proccessed)
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while processing clothes liked.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def procced_order(self, order: Order) -> Response:
        try:
            db = Database()
            payment = StripePayment()
            print(order.clothes_dict)
            order_id = db.insert_order(
                order=order, order_status='CREATING_PAYMENT_INTENT')

            card = db.select_credit_card_data(card_id=order.credit_card_id)

            customer = db.get_info_user(id_user=order.id_user)

            payment_intent_id = payment.create_payment_intent(
                order=order, customer=customer, card=card)
            logging.info(
                f'Created with success payment intetn with id {payment_intent_id}')
            if payment.confirm_payment_intent(payment_intent_id=payment_intent_id) == 'succeeded':
                if db.update_order(order_id=order_id, order_status='SEARCHING_COURIER', payment_intent_id=payment_intent_id) is not None:

                    res = db.remove_all_clothes_from_the_bag(
                        id_user=customer.id)
                    ress = requests.get(
                        f'http://localhost:8081/api_v1/courier/search_courier/{order_id}')
                    return Response(
                        json.dumps(
                            {
                                "status": 200,
                                "message": "OK",
                                "payload": None

                            }
                        ),
                        status=200,
                        mimetype="application/json"
                    )
                else:
                    return Response(
                        json.dumps(
                            {
                                "status": 501,
                                "message": "Failed to update status of order inside DB",
                                "payload": None

                            }
                        ),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                if db.update_order(order_id=order_id, order_status='CONFIRMATION_PAYMENT_FAILED'):

                    return Response(
                        json.dumps(
                            {
                                "status": 200,
                                "message": "Selected with success clothes",
                                "payload": None

                            }
                        ),
                        status=200,
                        mimetype="application/json"
                    )
                else:
                    return Response(
                        json.dumps(
                            {
                                "status": 501,
                                "message": "Failed to insert payment inside DB",
                                "payload": None

                            }
                        ),
                        status=200,
                        mimetype="application/json"
                    )

            # TODO SELECT ORDERS IN THE BAG OF THE CUSTOMER,INSERT INSIDE DB ORDER ENTITY WITH STATUS dePENDING ON DIFFERENT STAGE OF ORDER, CREATE PAYMENT_INTENT, CONFIRM PAYMENT, INSERT COURIER WICH WILL PROVIDE DELIVERY

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while add to DB clothe liked.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def add_quantity(self, id_user: int, id_clothe: str):
        try:
            db = Database()
            if db.add_quantity_clothe_in_the_bag(id_user=id_user, id_clothe=id_clothe):
                return Response(
                    json.dumps(
                        {
                            "status": 201,
                            "message": "Added quantity with success",
                            "payload": None

                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 500,
                            "message": "Failed to insert payment inside DB",
                            "payload": None

                        }
                    ),
                    status=500,
                    mimetype="application/json"
                )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def remove_quantity(self, id_user: int, id_clothe: str):
        try:
            db = Database()
            if db.remove_quantity_clothe_in_the_bag(id_user=id_user, id_clothe=id_clothe):
                return Response(
                    json.dumps(
                        {
                            "status": 201,
                            "message": "Removed quantity with success",
                            "payload": None

                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 500,
                            "message": "Failed to insert payment inside DB",
                            "payload": None

                        }
                    ),
                    status=500,
                    mimetype="application/json"
                )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_orders(self, id_user: int):
        try:
            orders_obj = Database().select_orders(id_user=id_user)
            print(orders_obj)
            final_res = []
            for order in orders_obj:
                obj_dict = {}
                obj_dict['status'] = order.status
                obj_dict['id_order'] = order.id
                obj_dict['street'] = order.street_delivery
                obj_dict['city'] = order.city
                obj_dict['hour'] = order.hour_delivery
                obj_dict['day'] = order.day_delivery
                obj_dict['amount'] = float(order.amount)
                quantity = 0
                for clothe in order.clothes:
                    quantity += clothe['quantity']
                obj_dict['quantity'] = quantity
                final_res.append(obj_dict)
            print(final_res)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": final_res

                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_order_clothes(self, id_order):
        try:
            order_clothes = Database().select_order_clothes(id_order=id_order)
            print(order_clothes)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": order_clothes

                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_clothes_to_return(self, id_user):
        try:
            clothes = Database().select_clothes_to_return(id_user=id_user)
            final_list = []
            for clothes_list in clothes:
                for clothe_dict in clothes_list.clothes:
                    if clothe_dict['returned'] == False:
                        clothe_dict['id_order'] = clothes_list.id
                        final_list.append(
                            clothe_dict
                        )
            print(final_list)

            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload": final_list

                    }
                ),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )
            

    def procced_order_return(self, order: Order):
        try:
            order_id = Database().insert_order(
                order=order, order_status='CREATING_PAYMENT_INTENT')
            print(order_id)

            card = Database().select_credit_card_data(card_id=order.credit_card_id)

            customer = Database().get_info_user(id_user=order.id_user)

            payment_intent_id = StripePayment().create_payment_intent(
                order=order, customer=customer, card=card)
            logging.info(
                f'Created with success payment intetn with id {payment_intent_id}')
            if StripePayment().confirm_payment_intent(payment_intent_id=payment_intent_id) == 'succeeded':
                if Database().update_order(order_id=order_id, order_status='SEARCHING_COURIER_REFUND_CLOTHES', payment_intent_id=payment_intent_id) is not None:
                    for clothe in order.clothes_dict:
                        Database().remove_clothe_from_order(order_id= clothe['id_order'],clothe_id=clothe['id'])
                    
                    res = requests.get(
                        f'http://localhost:8081/api_v1/courier/search_courier/{order_id}')
                    return Response(
                        json.dumps(
                            {
                                "status": 200,
                                "message": "Selected with success clothes",
                                "payload": None

                            }
                        ),
                        status=200,
                        mimetype="application/json"
                    )

                else:
                    if db.update_order(order_id=order_id, order_status='CONFIRMATION_PAYMENT_FAILED'):
                        return Response(
                            json.dumps(
                                {
                                    "status": 200,
                                    "message": "Selected with success clothes",
                                    "payload": None

                                }
                            ),
                            status=200,
                            mimetype="application/json"
                        )
            else:
                return Response(
                    json.dumps(
                        {
                            "status": 501,
                            "message": "Failed to insert payment inside DB",
                            "payload": None

                        }
                    ),
                    status=200,
                    mimetype="application/json"
                )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def procced_make_refund(self, order_id):
        try:
            order_info = Database().select_order_info(order_id=order_id)
            for clothe in order_info.clothes:
                order_clothe_refund = Database().select_order_info(
                    order_id=clothe['id_order'])
                if StripePayment().make_refund_money(order=order_clothe_refund) == 'succeeded':
                    logging.info(
                        f'Refund with success money width payment intent: {order_clothe_refund.stripe_id_intent}')
                else:
                    _logger.log('e', logger.LogLevel.error,
                                message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK"
                    }
                ),
                status=200,
                mimetype="application/json"
            )

        except Exception as e:
            _logger.log(e, logger.LogLevel.error,
                        message=f'An errore occured while adding quantity to clothe inside DB.')
            return Response(
                json.dumps(
                    {
                        "status": 500,
                        "message": "Internal server error."
                    }
                ),
                status=500,
                mimetype="application/json"
            )
