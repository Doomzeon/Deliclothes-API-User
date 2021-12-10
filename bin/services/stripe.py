from bin.models.order_entity import OrderEntity
from bin.utils.data_classes import CrediCard, Customer
from bin.models.user_entity import UserEntity
import stripe
import bin.utils.logger as logger  # import LogLevel, Logger

_logger = logger.Logger()


class Stripe:

    def __init__(self):
        self.__api_secret_key = "sk_test_51IXpOuHRpyaXtqnWypNdkx3YmbKxTVNzxRiscZEcWSj2pjOcwN2S1Z4ye8zAEMnmZacDOTRWoIggRhrgJAWv4JNi00yV2oVIvF"
        self.__api_public_key = "pk_test_51IXpOuHRpyaXtqnWbQX6536bkSptne8D3eacQRWnSzaEnza0lrx5j8GpLFIx5qJ4AZNjoc2IDEusf1fNRn5oZzpf00OP5SAbUq"

    def connect_card_to_user(self, user_id_stripe: str, credit_card_id_stripe: str):
        try:
            stripe.api_key = self.__api_secret_key
            stripe.PaymentMethod.attach(
                credit_card_id_stripe,
                customer=user_id_stripe
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An errore occured while conecting card to user on Stripe')
            raise(e)
        
        
        
    def confirm_payment_intent(self, id:str)->bool:
        try:
            stripe.api_key = self.__api_secret_key
           # logging.info(f'Trying to confirm payment intent with id: {payment_intent_id}')
            response = stripe.PaymentIntent.confirm(
                id
                )
            print(f"Confirmed with success payment intent {id} status: {response['status']}")
            return response['status']
        
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Errore occured while confirm payment')
            raise(e)

    def make_refund(self, order: OrderEntity):
        try:
            stripe.api_key = self.__api_secret_key
            amount = 0.0

            for clothe in order.clothes:
                amount += clothe['cost']
            response = stripe.Refund.create(
                payment_intent=order.stripe_id_intent,
                amount=int(amount*100)
            )
            return response['status']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An errore occured while making refund of money on stripe')
            raise(e)

    def create_payment_intent(self, email: str, id_customer: str, id_card: str, amount: int):
        try:
            stripe.api_key = self.__api_secret_key
            response_stripe = stripe.PaymentIntent.create(
                amount=amount*100,
                currency="eur",
                payment_method=id_card,
                description=f"Payment Intent of {id_customer} with {id_card} card",
                customer=id_customer,
                receipt_email=email
            )
            return response_stripe['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Error occured while creating payment intetnt')
            raise(e)

    def create_stripe_customer(self, user: Customer) -> str:
        try:
            stripe.api_key = self.__api_secret_key
           # logging.info(f'Contacting Stripe to create new Customer: {user}')
            response_stripe = stripe.Customer.create(
                description='customer.description',
                email=user.email,
                name=user.name
            )
          #  logging.info(f"Created with success new customer with id: {response_stripe['id']}")
            return response_stripe['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Error occured while creating strip costumer')
            raise(e)

    def add_new_credit_card(self, user: UserEntity, card: CrediCard):
        try:
            stripe.api_key = self.__api_secret_key
            response_stripe = stripe.PaymentMethod.create(
                type=card.card_type,
                card={
                    "number": card.card_number,  # "4242424242424242",
                    "exp_month": card.expiration_month,  # 3,
                    "exp_year": card.expiration_year,  # 2022,
                    "cvc": card.cvc  # "314",
                },
                billing_details={
                    "address": {
                        "city": user.city,
                        "country": 'it', #TODO change it!
                        "line1": user.residence,
                        "postal_code": user.zip_code,
                        "state": ''
                    },
                    "email": user.email,
                    "name": user.name,
                    "phone": user.country_code+'' + str(user.phone_number)
                }
            )
            return response_stripe['id']

        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'An errore occured while adding new card on stripe')
            raise(e)
