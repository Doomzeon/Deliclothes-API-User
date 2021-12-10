from enum import Enum 


class OrderSuccecedStatuses(Enum):
    creating_payment_intent = 0
    searching_for_the_courier = 1
    courier_found = 2
    delivery_in_progress = 3
    delivery_done = 4
    searching_for_the_courier_refund_clothes = 5
    confirmationf_payment_intent_failed = 6
    