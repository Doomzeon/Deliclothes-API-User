import logging
from bin.utils.data_classes import Customer, CrediCard, User, ClotheLiked, ClotheDataBag, Order
from bin.models import credit_card_entity, user_entity, clothes_liked_entity, clothes_bag_entity, order_entity
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import bin.utils.logger as logger  # import LogLevel, Logger

_logger = logger.Logger()


class Database:

    def __init__(self):
        self.__session = None

    def check_clothe_if_is_liked(self, id_clothe, id_user) -> bool:
        try:
            self.__session = self.__create_session()
            credit_card = self.__session.query(clothes_liked_entity.ClothesLiked).filter_by(
                id_clothe=str(id_clothe), id_user=int(id_user)).first()
            logging.info(f'\nSelected from Database: {credit_card}')
            if credit_card is not None:
                return True
            else:
                return False
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting data from the Database')
            return False
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_new_user(self, customer: Customer):
        try:
            self.__session = self.__create_session()
            logging.info(f'\nCreating user entity with {customer} data.')
            # TODO Crypt password
            user = user_entity.UserEntity(
                customer_id=customer.customer_id,
                email=customer.email,
                password=customer.password,
                name=customer.name,
                surname=customer.surname,
                phone_number=customer.phone_number,
                country_code=0,
                residence=customer.residence,
                language=customer.language,
                active=False,
                city=customer.city
            )
            logging.info(f'\nCreated with success UserEntity object ({user})')
            self.__session.add(user)
            self.__session.commit()
            self.__session.refresh(user)
            logging.info(
                f'\nCreated with success UserEntity object ({user.id})')
            return user.id
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding new user inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_credit_card_data(self, card_id: int):
        try:
            self.__session = self.__create_session()
            credit_card = self.__session.query(
                credit_card_entity.CreditCardEntity).filter_by(id=card_id).first()
            logging.info(f'\nSelected from Database: {credit_card}')
            return credit_card
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_user(self, id_user: int):
        try:
            logging.info(f'\nSelecting customer')
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user).first()
            logging.info(f'\nSelected from Database: {user}')
            return user
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting use data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def get_cards_user(self, id_user: int):
        try:
            logging.info(f'\nSelecting cards of user')
            self.__session = self.__create_session()
            cards = self.__session.query(
                credit_card_entity.CreditCardEntity).filter_by(user_id=id_user).all()
            logging.info(f'\nSelected from Database: {cards}')
            return cards
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting use data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_user_data(self, customer: Customer):
        try:
            logging.info(f'\nSelecting customer')
            self.__session = self.__create_session()
            user = self.__session.query(user_entity.UserEntity).filter_by(
                email=customer.email).first()
            logging.info(f'\nSelected from Database: {user}')
            return user
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting use data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def get_info_user(self, id_user: int):
        try:
            logging.info(f'\nSelecting customer')
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user).first()
            logging.info(f'\nSelected from Database: {user}')
            return user
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting user data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_user_data_login(self, user: User):
        try:
            logging.info(f'\nSelecting customer')
            self.__session = self.__create_session()
            user = self.__session.query(user_entity.UserEntity).filter_by(
                email=user.email, password=user.password).first()
            logging.info(f'\nSelected from Database: {user}')
            return user
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting user data from the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def like_clothe(self, clothe_liked: ClotheLiked):
        try:
            self.__session = self.__create_session()
            clothe = clothes_liked_entity.ClothesLiked(
                id_clothe=clothe_liked.id_clothe,
                id_user=clothe_liked.id_user,
                brand=clothe_liked.brand
            )
            logging.info(
                f'\nCreated with success ClotheLiked entity object ({clothe})')
            self.__session.add(clothe)
            self.__session.commit()
            logging.info(f'\nInserted with success ClotheLiked')
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def dislike_clothe(self, id_clothe: str, id_user: int):
        try:
            self.__session = self.__create_session()
            clothe = self.__session.query(clothes_liked_entity.ClothesLiked).filter_by(
                id_clothe=id_clothe, id_user=id_user).first()
            self.__session.delete(clothe)
            self.__session.commit()
            logging.info(
                f'Removed from the database clothe with id :{id_clothe}')
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while removing liked clothe inside the Database')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def add_clothe_to_the_bag(self, clothe_data_bag: ClotheDataBag):
        try:
            self.__session = self.__create_session()
            clothe = clothes_bag_entity.ClotheInTheBag(
                id_clothe=clothe_data_bag.id_clothe,
                id_user=clothe_data_bag.id_user,
                brand=clothe_data_bag.brand,
                size=clothe_data_bag.size,
                quantity=clothe_data_bag.quantity,
                id_size=clothe_data_bag.id_size
            )
            self.__session.add(clothe)
            self.__session.commit()
            logging.info(f'Added clothe to the bag {clothe}')
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding clothe to the bag inside Database')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_card(self, id_user, id_card):
        try:
            self.__session = self.__create_session()
            card = self.__session.query(credit_card_entity.CreditCardEntity).filter_by(
                user_id=id_user, id=id_card).first()
            self.__session.delete(card)
            self.__session.commit()
            logging.info(f'Removed with succes clothe from the bag with id ')
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
            return False
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_clothe_from_the_bag(self, id_clothe: str, id_user: int):
        try:
            self.__session = self.__create_session()
            clothe = self.__session.query(clothes_bag_entity.ClotheInTheBag).filter_by(
                id_clothe=id_clothe, id_user=id_user).first()
            self.__session.delete(clothe)
            self.__session.commit()
            logging.info(
                f'Removed with succes clothe from the bag with id {id_clothe}')
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
            return False
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
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while selecting data from the Database')
            self.__error_handling()
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
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_new_credit_card(self, customer: Customer):
        try:
            self.__session = self.__create_session()
            logging.info(
                f'\nCreating card entity with {customer.credit_card} data.')
            credit_card = credit_card_entity.CreditCardEntity(
                id_stripe=customer.credit_card.id_stripe,
                user_id=customer.id,
                title=customer.credit_card.title,
                expiration_month=customer.credit_card.expiration_month,
                expiration_year=customer.credit_card.expiration_year,
                cvc=customer.credit_card.cvc,
                card_number=customer.credit_card.card_number,
                card_type=customer.credit_card.card_type
            )
            logging.info(
                f'\nCreated with success CreditCardEntity object ({credit_card})')
            self.__session.add(credit_card)
            self.__session.commit()
            self.__session.refresh(credit_card)
            return credit_card.id
        except Exception as e:
            self.__error_handling()
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding credit card inside the Database')
            raise(e)
        finally:
            if self.__session is not None:
                self.__close_session()

    def insert_order(self, order: Order, order_status: str, stripe_id_intent: str = None):
        try:
            self.__session = self.__create_session()
            #logging.info(f'\nCreating card entity with {customer.credit_card} data.')
            order_ent = order_entity.OrderEntity(
                id_user=order.id_user,
                clothes=order.clothes_dict,
                hour_delivery=order.hour_delivery,
                day_delivery=order.day_delivery,
                status=order_status,
                street_delivery=order.street_delivery,
                credit_card_id=order.credit_card_id,
                amount=order.amount,
                stripe_id_intent=stripe_id_intent,
                city=order.city,
                zip_code=order.zip_code
            )
            #logging.info(f'\nCreated with success CreditCardEntity object ({credit_card})')
            self.__session.add(order_ent)
            self.__session.commit()
            self.__session.refresh(order_ent)
            logging.info('Inserted with success new order!')
            return order_ent.id
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding new data to the Database')
            self.__error_handling()
            return None
        finally:
            if self.__session is not None:
                pass
                self.__close_session()

    def update_order(self, order_id: int, order_status: str, payment_intent_id):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=order_id).first()
            order.status = order_status
            order.stripe_id_intent = payment_intent_id
            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding new data to the Database')
            self.__error_handling()
            return None
        finally:
            if self.__session is not None:
                pass
                self.__close_session()

    def add_quantity_clothe_in_the_bag(self, id_user: int, id_clothe: str):
        try:
            self.__session = self.__create_session()
            clothes = self.__session.query(clothes_bag_entity.ClotheInTheBag).filter_by(
                id_user=id_user, id_clothe=id_clothe).first()
            clothes.quantity += 1
            self.__session.commit()
            return True
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_quantity_clothe_in_the_bag(self, id_user: int, id_clothe: str):
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
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_all_clothes_from_the_bag(self, id_user):
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
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def modify_name(self, id_user: int, name: str):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user,).first()
            user.name = name
            self.__session.commit()

        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def modify_surname(self, id_user: int, surname: str):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user,).first()
            user.surname = surname
            self.__session.commit()

        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def modify_residence(self, id_user: int, residence: str):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user,).first()
            user.residence = residence
            self.__session.commit()

        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def modify_phone(self, id_user: int, phone: int):
        try:
            self.__session = self.__create_session()
            user = self.__session.query(
                user_entity.UserEntity).filter_by(id=id_user,).first()
            user.phone_number = phone
            self.__session.commit()

        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
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
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_order_clothes(self, id_order):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=id_order).first()
            return order.clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_payment_intent_order(self, order_id):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=order_id).first()
            return order.payment_intent_id
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_clothes_to_return(self, id_user):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(order_entity.OrderEntity).filter_by(
                id_user=id_user, status='DELIVERY_DONE').all()

            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def select_order_info(self, order_id):
        try:
            self.__session = self.__create_session()
            order = self.__session.query(
                order_entity.OrderEntity).filter_by(id=order_id).first()
            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
        finally:
            if self.__session is not None:
                self.__close_session()

    def remove_clothe_from_order(self, order_id, clothe_id):
        try:
            logging.info(clothe_id)
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
            print(order.clothes)
            self.__session.commit()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An error occured while adding liked clothe inside Database')
            self.__error_handling()
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
