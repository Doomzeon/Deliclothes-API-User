
import stripe
from bin.utils.data_classes import Customer, CrediCard, Order
import logging
import bin.utils.logger as logger #import LogLevel, Logger

_logger = logger.Logger()

class StripePayment:

    def __init__(self):
        self.__api_secret_key = "sk_test_51IXpOuHRpyaXtqnWypNdkx3YmbKxTVNzxRiscZEcWSj2pjOcwN2S1Z4ye8zAEMnmZacDOTRWoIggRhrgJAWv4JNi00yV2oVIvF"
        self.__api_public_key = "pk_test_51IXpOuHRpyaXtqnWbQX6536bkSptne8D3eacQRWnSzaEnza0lrx5j8GpLFIx5qJ4AZNjoc2IDEusf1fNRn5oZzpf00OP5SAbUq"

    def create_stripe_customer(self, customer:Customer) -> str:
        try:
            stripe.api_key = self.__api_secret_key
            logging.info(f'Contacting Stripe to create new Customer: {customer}')
            response_stripe = stripe.Customer.create(
                description='customer.description',
                email=customer.email,
                name=customer.name
            )
            logging.info(f"Created with success new customer with id: {response_stripe['id']}")
            return response_stripe['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Error occured while creating strip costumer')
            raise(e)
        
        
    def create_credit_card(self, customer):
        try:
            stripe.api_key = self.__api_secret_key
            logging.info(
                f'Adding new card to customer with id: {customer.customer_id}')
            response_stripe = stripe.PaymentMethod.create(
                type=customer.credit_card.card_type,
                card={
                    "number": customer.credit_card.card_number,  # "4242424242424242",
                    "exp_month": customer.credit_card.expiration_month,  # 3,
                    "exp_year": customer.credit_card.expiration_year,  # 2022,
                    "cvc": customer.credit_card.cvc  # "314",
                },  # "cus_JArF6tYkmVfV64"
                billing_details={
                        "address": {
                            "city": customer.city,
                            "country": customer.country,
                            "line1": customer.residence,
                            "postal_code": customer.zip_code,
                            "state": ''
                        },
                        "email": customer.email,
                        "name": customer.name,
                        "phone": customer.country_code+''+ str(customer.phone_number)
                }
                )
            logging.info(f"Added with success new card with id: {response_stripe['id']} to customer({customer.customer_id})")
            return response_stripe['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'An errore occured while adding new card on stripe')
            raise(e)
        
    def add_credit_card_to_customer(self, customer:Customer):
        try:
            stripe.api_key = self.__api_secret_key
            stripe.PaymentMethod.attach(
                customer.credit_card.id_stripe,
                customer=customer.customer_id
            )
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Errore occured during adding credit card to the user on stripe')
            raise(e)


    def create_payment_intent(self, order:Order, customer, card):
        try:
            stripe.api_key = self.__api_secret_key
            #TODO add taxes
            #TODO add shipping details
            logging.info(f'Trying to create paymentIntent for {customer.customer_id}')
            response_stripe = stripe.PaymentIntent.create(
                amount=order.amount*100,
                currency="eur",
                payment_method=card.id_stripe,
                description=f"Payment Intent of {customer.customer_id} with {card.id_stripe} card",
                customer=customer.customer_id,
                receipt_email=customer.email
                )
            logging.info(f"Created with success payment intent with id {response_stripe['id']}")
            return response_stripe['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Errore occured while creating strip costumer')
            raise(e)


    def confirm_payment_intent(self, payment_intent_id:str)->bool:
        try:
            stripe.api_key = self.__api_secret_key
            logging.info(f'Trying to confirm payment intent with id: {payment_intent_id}')
            response = stripe.PaymentIntent.confirm(
                payment_intent_id
                )
            logging.info(f"Confirmed with success payment intent {payment_intent_id} status: {response['status']}")
            return response['status']
        
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Errore occured while confirm payment')
            raise(e)


    def make_refund_money(self, order)->bool:
        try:
            stripe.api_key = self.__api_secret_key
            #logging.info(f'Trying to confirm payment intent with id: {payment_intent_id}')
            amount = 0.0
            print(order.clothes)
            
            for clothe in order.clothes:
                print(clothe)
                amount+=clothe['cost']
            logging.info(f'Refund amount: {amount*100}')
            response = stripe.Refund.create(
                    payment_intent=order.stripe_id_intent,
                    amount=int(amount*100)
                    )
            logging.info(f"Confirmed with success payment intent status: {response['status']}")
            return response['status']
        
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Errore occured while confirm payment')
            raise(e)
