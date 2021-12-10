import datetime
import logging

from sqlalchemy.sql.expression import false
from bin.utils.data_classes import Customer, CrediCard, User, ClotheLiked, ClotheDataBag, Order, UserMMDScheleton
from bin.models import credit_card_entity, user_entity, clothes_liked_entity, clothes_bag_entity, order_entity, posters_entity, shop_model_entity, shop_order_entity
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import bin.utils.logger as logger  # import LogLevel, Logger

_logger = logger.Logger()


class Database:

    def __init__(self):
        self.__session = None

    def select_order(self, order_id: int):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=order_id).first()
            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'DB errore while selecting orders')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
                
    def select_gender_user(self, id_user:int):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user).first()
            
            return user.gender
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'DB errore while selecting gender of the user')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_posters(self):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(posters_entity.PostersEntity).all()
            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting posters')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def change_status_returned_clothe_inside_order(self, order_id: int, clothe_id):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=order_id).first()
            for i in range(len(order.clothes)):
                if order.clothes[i]['id'] == clothe_id:
                    a = order.clothes[i]
                    a['returned'] = True
                    del order.clothes[i]
                    order.clothes.append(a)
                    break
            self.__session.commit()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while chaging status of returned clothes inside order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_clothes_inside_the_order(self, id_order: int = None):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=id_order).first()
            return order.clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting clothes inside the order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_orders_delivered(self, id_user: int):
        try:
            self.__session = self.__create_session()
            orders = self.__session.query(order_entity.OrderEntity).filter_by(
                id_user=id_user, status_int=3).all()
            return orders
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting delivered orders')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_orders(self, id_user: int):
        try:
            self.__session = self.__create_session()
            orders = self.__session.query(
                order_entity.OrderEntity).filter_by(id_user=id_user).all()
            return orders
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting orders')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_card(self, id_card: int):
        try:
            self.__session = self.__create_session()
            credit_card = self.__session.query(
                credit_card_entity.CreditCardEntity).filter_by(id=id_card).first()
            logging.info(f'\nSelected from Database: {credit_card}')
            return credit_card.id_stripe
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selectin cards ')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def update_status_order(self, id_order: int, status: int, payment_intent_id: str = None):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=id_order).first()
            order.status_int = status
            if order.stripe_id_intent is not None:
                order.stripe_id_intent = payment_intent_id
            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while updting status of order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_order(self, order: Order, status: int):
        try:
            self.__session = self.__create_session()
            #logging.info(f'\nCreating card entity with {customer.credit_card} data.')
            order_ent = order_entity.OrderEntity(
                id_user=order.id_user,
                clothes=order.clothes_dict,
                hour_delivery=order.hour_delivery,
                day_delivery=order.day_delivery,
                status=status,
                street_delivery=order.street_delivery,
                credit_card_id=order.credit_card_id,
                amount=order.amount,
                city=order.city,
                zip_code=order.zip_code,
                end= datetime.datetime.strptime(order.day_delivery +'T' + order.hour_delivery, "%Y-%m-%dT%H:%M%p")
            )
            #logging.info(f'\nCreated with success CreditCardEntity object ({credit_card})')
            self.__session.add(order_ent)
            self.__session.commit()
            self.__session.refresh(order_ent)
            logging.info('Inserted with success new order!')
            return order_ent.id
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def add_quantity_clothe(self, id_user: int, id_clothe: str):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(clothes_bag_entity.ClotheInTheBag).filter_by(
                id_user=id_user, id_clothe=id_clothe).first()
            clothes.quantity += 1
            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding quantity to the clothe')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_quantity_clothe(self, id_user: int, id_clothe: str):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(clothes_bag_entity.ClotheInTheBag).filter_by(
                id_user=id_user, id_clothe=id_clothe).first()
            if clothes.quantity == 1:
                self.__session.delete(clothes)
            else:
                clothes.quantity -= 1
            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while removing quantity of the clothe')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def delete_clothes_from_the_bag(self, id_user: int):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(
                clothes_bag_entity.ClotheInTheBag).filter_by(id_user=id_user).all()
            if isinstance(clothes, list):
                for clothe in clothes:
                    self.__session.delete(clothe)
            else:
                self.__session.delete(clothes)

            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while removing clothes from the bag ')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def delete_clothe_from_the_bag(self, id_clothe: str, id_user: int):
        try:
            self.__session = self.__create_session()
            clothe = self.__session.query(clothes_bag_entity.ClotheInTheBag).filter_by(
                id_clothe=id_clothe, id_user=id_user).first()
            self.__session.delete(clothe)
            self.__session.commit()
            return True
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while deleting clothe from the bag ')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_liked_clothes(self, id_user: int):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(
                clothes_liked_entity.ClothesLiked).filter_by(id_user=id_user).all()
            return clothes
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting liked clothes')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_clothes_in_the_bag(self, id_user: int):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(
                clothes_bag_entity.ClotheInTheBag).filter_by(id_user=id_user).all()
            return clothes
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting clothes in the bag')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_clothe_inside_the_bag(self, clothe: ClotheDataBag):
        try:
            self.__session = self.__create_session()
            clothe_ent = clothes_bag_entity.ClotheInTheBag(
                id_clothe=clothe.id_clothe,
                id_user=clothe.id_user,
                brand=clothe.brand,
                size=clothe.size,
                quantity=clothe.quantity,
                id_size=clothe.id_size
            )
            self.__session.add(clothe_ent)
            self.__session.commit()

            return True

        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting clothes inside the bag ')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_liked_clothe(self, id_clothe: str, id_user: int):
        try:
            self.__session = self.__create_session()
            clothe_ent = self.__session.query(clothes_liked_entity.ClothesLiked).filter_by(
                id_clothe=id_clothe, id_user=id_user).first()
            self.__session.delete(clothe_ent)
            self.__session.commit()
            return True

        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while removing liked clothe ')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_liked_clothe(self, clothe: ClotheLiked):
        try:
            self.__session = self.__create_session()
            clothe_ent = clothes_liked_entity.ClothesLiked(
                id_clothe=clothe.id_clothe,
                id_user=clothe.id_user,
                brand=clothe.brand
            )
            self.__session.add(clothe_ent)
            self.__session.commit()
            return True
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting clothe liked')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_new_user(self, user: Customer):
        try:
            self.__session = self.__create_session()
            logging.info(f'\nCreating user entity with {user} data.')
            # TODO Crypt password
            user = user_entity.UserEntity(
                customer_id=user.customer_id,
                email=user.email,
                password=user.password,
                name=user.name,
                surname=user.surname,
                phone_number=user.phone_number,
                country_code=0,
                residence=user.residence,
                language=user.language,
                active=False,
                gender=user.gender,
                city=user.city
            )
            self.__session.add(user)
            self.__session.commit()
            self.__session.refresh(user)
            return user
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting new user')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_user_id(self, user: User):
        try:
            self.__session = self.__create_session()
            user_ent = self.__session.query(user_entity.UserEntity).filter_by(
                email=user.email, password=user.password).first()
            return user_ent
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting user id from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def delete_card(self, id_user: int, id_card: int):
        try:
            self.__session = self.__create_session()
            card = self.__session.query(credit_card_entity.CreditCardEntity).filter_by(
                user_id=id_user, id=id_card).first()
            self.__session.delete(card)
            self.__session.commit()
            return True

        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while deleting the card  from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_card(self, id_user: int, card: CrediCard):
        try:
            self.__session = self.__create_session()
            credit_card = credit_card_entity.CreditCardEntity(
                id_stripe=card.id_stripe,
                user_id=id_user,
                title=card.title,
                expiration_month=card.expiration_month,
                expiration_year=card.expiration_year,
                cvc=card.cvc,
                card_number=card.card_number,
                card_type=card.card_type
            )
            self.__session.add(credit_card)
            self.__session.commit()
            self.__session.refresh(credit_card)
            return credit_card.id
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting  card inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_user(self, id_user: int = None, email: str = None, password: str = None):
        try:
            self.__session = self.__create_session()
            if id_user is not None:
                user = self.__session.query(
                    user_entity.UserEntity).filter_by(id=id_user).first()
                return user
            else:
                user = self.__session.query(
                    user_entity.UserEntity).filter_by(email=email, password=password).first()
                return user

        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting user data')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_cards(self, id_user: int):
        try:
            self.__session = self.__create_session()
            cards = self.__session.query(
                credit_card_entity.CreditCardEntity).filter_by(user_id=id_user).all()
            return cards
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting cards')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def update_main_info(self, user: UserMMDScheleton):
        try:
            self.__session = self.__create_session()
            user_ent = self.__session.query(
                user_entity.UserEntity).filter_by(id=user.id).first()
            if user.name is not None:
                user_ent.name = user.name
            if user.surname is not None:
                user_ent.surname = user.surname
            if user.phone.phone is not None:
                user_ent.phone_number = user.phone.phone
            if user.phone.code is not None:
                user_ent.country_code = user.phone.code
            if user.residence is not None:
                user_ent.residence = user.residence

            self.__session.commit()
            return True
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while updating main info of the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()
                
    def is_clothe_liked(self, id_user:int, id_clothe:int):
        try:
            self.__session = self.__create_session()
            clothe_ent = self.__session.query(clothes_liked_entity.ClothesLiked).filter_by(
                id_clothe=str(id_clothe), id_user=id_user).first()
            if clothe_ent is not None:
                return True
            else:
                return False
            
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while updating main info of the Database')
            raise(e)
    
    
    def select_shop_by_id(self, id_shop:int):
        try:
            self.__session = self.__create_session()
            shop_ent = self.__session.query(shop_model_entity.Shop).filter_by(
                id=id_shop).first()
            return shop_ent
            
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting info about shop by id from the Database')
            raise(e)            

    
    
    
    def insert_order_shop(self, id_order, id_shop, prepare_to, clothes):
        try:
            self.__session = self.__create_session()
            shop_order_ent = shop_order_entity.ShopOrder(
                idShop=id_shop,
                idOrder=id_order,
                prepare_to=prepare_to,
                clothes=clothes
            )
            #logging.info(f'\nCreated with success CreditCardEntity object ({credit_card})')
            self.__session.add(shop_order_ent)
            self.__session.commit()
            logging.info('Inserted with success new order inside the shop orders table!')
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while inserting order inside order shops table Database')
            raise(e) 
        
        
    def update_start_time_order(self, id, start):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=id).first()
            order.start = start
            self.__session.commit()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while updting status of order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def update_directions(self, id, directions):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=id).first()
            order.directions = directions
            self.__session.commit()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while updting status of order')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def __error_handling(self):
        self.__session.rollback()
        self.__close_session()

    def __close_session(self):
        if self.__session is not None:
            self.__session.close()

    def __create_session(self):
        try:
            logging.info('\nCreating session object with the Database')
            Session = sessionmaker(
                bind=self.__get_db_engine(), expire_on_commit=False)
            return Session()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An errore occured while creating session with the Database')
            raise(e)

    def __get_db_engine(self):
        try:
            logging.info('\nConnecting to the Database')
            engine = sqlalchemy.create_engine(
                "postgresql+psycopg2://doomzeon:doomzeon@localhost/doomzeon", pool_pre_ping=True)

            logging.info("\nConnection with the Database established")
            return engine
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Fail to establish connection with the database')
            raise(e)
