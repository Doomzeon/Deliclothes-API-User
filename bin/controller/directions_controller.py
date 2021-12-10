import itertools
from bin.services.database_new import Database
from bin.services.db_mongo import DatabaseMD
import logging
from bin.services.zara_new import Zara
from logging import exception, log
import json
import bin.utils.logger as logger
from flask import Response
import requests
from bin.services.mapbox import MapBox
from bin.services.zara_new import Zara
from itertools import permutations
import numpy as np
import datetime

_logger = logger.Logger()

shops_milan_zara = [
    {
        "id": 3307,
        "lng": 9.18795235,
        "lat": 45.46365356
    }, {
        "id": 3197,
        "lng": 9.19308,
        "lat": 45.46478
    }, {
        "id": 9720,
        "lng": 9.195836,
        "lat": 45.464604
    }, {
        "id": 9105,
        "lng": 9.20353984,
        "lat": 45.48534011
    }, {
        "id": 3327,
        "lng": 9.21214,
        "lat": 45.48152
    }, {
        "id": 3530,
        "lng": 9.145512,
        "lat": 45.490436
    }, {
        "id": 12859,
        "lng": 9.15290946,
        "lat": 45.40382728
    }, {
        "id": 9123,
        "lng": 9.17594,
        "lat": 45.3923
    }, {
        "id": 3529,
        "lng": 9.257162,
        "lat": 45.549881
    }, {
        "id": 3391,
        "lng": 9.329978,
        "lat": 45.545459
    }, {
        "id": 3198,
        "lng": 9.274746,
        "lat": 45.583996
    }, {
        "id": 6437,
        "lng": 9.052627,
        "lat": 45.563084
    }, {
        "id": 3307,
        "lng": 9.473734,
        "lat": 45.620472
    },

]


test_list_shops = [
    {
        "id_shop": 3197,
        "lat": 9.19308,
        "lng": 45.46478,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 9105,
        "lat": 9.20353984,
        "lng": 45.48534011,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 3327,
        "lat": 9.21214,
        "lng": 45.48152,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 3530,
        "lat": 9.145512,
        "lng": 45.490436,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 12859,
        "lat": 9.15290946,
        "lng": 45.40382728,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 9123,
        "lat": 9.17594,
        "lng": 45.3923,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 3529,
        "lat": 9.257162,
        "lng": 45.549881,
        "clothes_ids": [
            "78527013"
        ]
    },
    {
        "id_shop": 3391,
        "lat": 9.329978,
        "lng": 45.545459,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    },
    {
        "id_shop": 6437,
        "lat": 9.052627,
        "lng": 45.563084,
        "clothes_ids": [
            "91407497",
            "78524316"
        ]
    }
]


class DirectionsController:

    def calculate_unavailable_times(self, id_user: int):
        try:
            less_duration_mileeseconds, less_duration_timestapm, win_combination = None, None, None
            # STEP 1 => Get a obj with id clothe and shops when i can find the clothe
            clothe_with_shops_ids_list = self.__find_clothe_shops(
                id_user=id_user)
            logging.info(clothe_with_shops_ids_list)
            # STEP 2 => Find shops when i can gat more than 1 clothe if i can rebuild dict
            rebuilded_clothe_shops_dict = self.__find_same_shops_of_clothes(
                clothe_with_shops_ids_list=clothe_with_shops_ids_list)
            # STEP 3 => Find if there is a shop which can take all clothe or not
            shop_all_clothes_founded, shop_clothes = self.__find_same_shop(rebuilded_clothe_shops_dict= rebuilded_clothe_shops_dict, clothes_len= len(clothe_with_shops_ids_list))
            # STEP 4 => If there is not shop where i can take all clothes build new dictionary with combinations different of the shops to calculate after directions
            if shop_all_clothes_founded == False:
                final_list_combinations_shops_clothes = self.__build_combinations_of_shops_on_which_to_take_order(rebuilded_clothe_shops_dict=rebuilded_clothe_shops_dict)
            # STEP 5 => Comvintaoin of shops directions
                combinations_shops_ids = self.__make_combination_of_directions(
                    final_list_combinations_shops_clothe=final_list_combinations_shops_clothes)
            # STEP 6 => If there is more than 1 shop when i can take order calculate duration from the start point when the courier have to start
            # STEP 6 => to find which shop will be more near
                less_duration_mileeseconds, less_duration_timestapm, win_combination = self.__calculate_more_fast_direction(
                    combinations_shops_ids=combinations_shops_ids, shops=shops_milan_zara)
            else:
                less_duration_mileeseconds, less_duration_timestapm = MapBox().calculate_directions(lat_lng_list=[{"lat":shop_clothes[0]['lng'], 'lng':shop_clothes[0]['lat']}])
                win_combination = shop_clothes[0]
            # STEP 7 => Go and select all orders grouped by coruirer in order ASC
            all_list_couriers_orders_times_grouped = DatabaseMD().select_orders_order_by_time_asc_and_group_by_couriers()
            # STEP 8 => Find time on which delivery can not be performed 
            times_unavailable = self.__process_times( list_couriers_orders_times=all_list_couriers_orders_times_grouped, duration_win_combination=less_duration_mileeseconds)
            logging.info(f'Times unavailable => {times_unavailable}')
            return Response(self.__build_payload_response(message='OK', payload={'time_unavailable':times_unavailable, 'directions':win_combination}), status=200, mimetype="application/json")
        except Exception as e:
            logging.error(e)
            
    def __build_payload_response(self, message: str, payload=None) -> dict:
        return json.dumps({
            "message": message,
            "payload": payload
        })

    def __calculate_more_fast_direction(self, combinations_shops_ids, shops):
        try:
            less_duration_mileeseconds, less_duration_timestapm = None, None
            win_combination = None
            for combination_items in combinations_shops_ids:
                lat_lng_list = []
                for combination_item in combination_items:

                    shop_obj = list(filter(
                        lambda item: item['id'] == combination_item, shops))
                    lat_lng_list.append(shop_obj[0])

                duration, timestamp_duration = MapBox(
                ).calculate_directions(lat_lng_list=lat_lng_list)
                print(timestamp_duration)
                if less_duration_timestapm is None and less_duration_mileeseconds is None:
                    less_duration_mileeseconds = duration
                    less_duration_timestapm = timestamp_duration
                    win_combination = combination_items
                else:
                    if duration < less_duration_mileeseconds:
                        less_duration_mileeseconds = duration
                        less_duration_timestapm = timestamp_duration
                        win_combination = combination_items
            print(f'less_duration_mileeseconds {less_duration_mileeseconds}')
            print(f'less_duration_timestapm {less_duration_timestapm}')
            print(f'win_combination {win_combination}')
            win_combination_shops = []
            for item in win_combination:
                shop_obj = list(filter(
                        lambda item: item['id'] == combination_item, shops))
                win_combination_shops.append(shop_obj)
            return less_duration_mileeseconds, less_duration_timestapm, win_combination_shops
        except Exception as e:
            print(e)

    def __make_combination_of_directions(self, final_list_combinations_shops_clothe):
        try:
            d_list_shops_ids = []
            for clothe in final_list_combinations_shops_clothe:
                d_list_shops_ids.append(clothe['shops_ids'])
            a = list(itertools.product(*d_list_shops_ids))
            print(a)
            return a

        except Exception as e:
            print(e)

    def __build_combinations_of_shops_on_which_to_take_order(self, rebuilded_clothe_shops_dict):
        try:
            print('asss')
            new_list = []
            for shop in rebuilded_clothe_shops_dict:
                print(shop)
                if len(new_list) <= 0:
                    print('i')
                    new_list.append({
                        "clothes_ids": shop['clothes_ids'],
                        "shops_ids": [
                            shop['id_shop']
                        ]
                    })
                elif len(new_list) > 0:
                    print(len(new_list))
                    for index, item_new_list in enumerate(new_list):
                        print(shop['id_shop']
                              not in item_new_list['shops_ids'])
                        if len(np.setdiff1d(shop['clothes_ids'], item_new_list['clothes_ids'])) <= 0 and shop['id_shop'] not in item_new_list['shops_ids']:
                            new_list[index]['shops_ids'].append(
                                shop['id_shop'])
                            break
                        elif len(np.setdiff1d(shop['clothes_ids'], item_new_list['clothes_ids'])) > 0 and shop['id_shop'] not in item_new_list['shops_ids']:
                            print(np.setdiff1d(
                                shop['clothes_ids'], item_new_list['clothes_ids']))
                            print('rttt')
                            print(f'new list {new_list}')
                            new_list.append({
                                "clothes_ids": shop['clothes_ids'],
                                "shops_ids": [
                                    shop['id_shop']
                                ]
                            })
                            break
                else:
                    continue
            logging.info(f'new list => {new_list}')
            return new_list
        except Exception as e:
            print(e)

    def __find_same_shop(self, rebuilded_clothe_shops_dict, clothes_len):
        try:
            logging.info(f'Truing to find same shop with the same clothes')
            shop_with_same_clothes = []
            founded = False
            for shop in rebuilded_clothe_shops_dict:
                if len(shop['clothes_ids']) == clothes_len:
                    shop_with_same_clothes.append(shop)
                    founded = True

            logging.info(
                f'founded: {founded}, shop_with_same_clothes: {shop_with_same_clothes}')
            return founded, shop_with_same_clothes
        except Exception as e:
            print(e)

    def __find_same_shops_of_clothes(self, clothe_with_shops_ids_list: list):
        try:
            logging.info(F'Trying to find same shop')
            logging.info(clothe_with_shops_ids_list)
            rebuilded_list_dict_clothes_shops = []
            for clothe in clothe_with_shops_ids_list:
                other_clothes = list(filter(
                    lambda item: item['id_clothe'] != clothe['id_clothe'], clothe_with_shops_ids_list))
                for shop in clothe['shops']:
                    for other_clothe in other_clothes:
                        same_shop = list(
                            filter(lambda item: item['id'] == shop['id'], other_clothe['shops']))
                        if len(same_shop) > 0:
                            logging.info(f'Same shop=> {same_shop}')
                            if len(rebuilded_list_dict_clothes_shops) <= 0:
                                rebuilded_list_dict_clothes_shops.append({
                                    'id_shop': same_shop[0]['id'],
                                    'lat': same_shop[0]['lng'],
                                    'lng': same_shop[0]['lat'],
                                    'clothes_ids': [
                                        clothe['id_clothe']
                                    ]
                                })
                            elif len(rebuilded_list_dict_clothes_shops) > 0 and len(list(filter(lambda item: item['id_shop'] == same_shop[0]['id'], rebuilded_list_dict_clothes_shops))) == 0:
                                rebuilded_list_dict_clothes_shops.append({
                                    'id_shop': same_shop[0]['id'],
                                    'lat': same_shop[0]['lng'],
                                    'lng': same_shop[0]['lat'],
                                    'clothes_ids': [
                                        clothe['id_clothe']
                                    ]
                                })
                            elif len(rebuilded_list_dict_clothes_shops) > 0 and len(list(filter(lambda item: item['id_shop'] == same_shop[0]['id'], rebuilded_list_dict_clothes_shops))) > 0:

                                for rebuilded_list_dict_clothe_shop in rebuilded_list_dict_clothes_shops:
                                    if rebuilded_list_dict_clothe_shop['id_shop'] == same_shop[0]['id'] and len(list(filter(lambda item: item == clothe['id_clothe'], rebuilded_list_dict_clothe_shop['clothes_ids']))) == 0:
                                        rebuilded_list_dict_clothe_shop['clothes_ids'].append(
                                            clothe['id_clothe']
                                        )

            logging.info(
                f'rebuilded_list_dict_clothes_shops {rebuilded_list_dict_clothes_shops}')
            return rebuilded_list_dict_clothes_shops
        except Exception as e:
            print(e)

    def __find_clothe_shops(self, id_user: int):
        try:
            logging.info(f'Selecting clothe in the bag of the user {id_user}')
            clothes_bag = Database().select_clothes_in_the_bag(id_user=id_user)
            logging.info(f"Clothes inside the bag : {clothes_bag}")
            zara = Zara(language="it")
            clothe_with_shops_ids_list = []
            for clothe in clothes_bag:
                refer_id_product, size_id = zara.get_refer_id_of_the_clothe_by_size(
                    id_clothe=clothe.id_clothe, selected_size=clothe.size)
                logging.info(
                    f'Refer_id_product: {refer_id_product}, size id {size_id}')
                product_availality_shops_ids = zara.get_product_availability_in_shops(
                    reference_id_product_without_id_size=refer_id_product, id_size=size_id)
                logging.info(
                    f'product_availality_shops_ids : {product_availality_shops_ids}')
                shops_list = []
                for shop in product_availality_shops_ids:
                    shop_obj = list(filter(
                        lambda item: item['id'] == shop['shop_id'], shops_milan_zara))
                    if len(shop_obj) > 0:
                        shops_list.append(shop_obj[0])
                clothe_with_shops_ids_list.append(
                    {"id_clothe": clothe.id_clothe, "shops": shops_list}
                )

            return clothe_with_shops_ids_list
        except Exception as e:
            logging.error(e)

    def __process_times(self, list_couriers_orders_times: list, duration_win_combination):
        try:
            list_orders_courier_to_calculate_unvavailable_time = []
            for courier in list_couriers_orders_times:
                for index_order, order_courier in enumerate(courier['orders']):
                    if index_order + 1 < len(courier['orders']):
                        difference_orders = courier['orders'][index_order +
                                                              1]['time_start'] - order_courier['time_end']
                        if difference_orders.seconds + 900 < duration_win_combination:
                            print(
                                f"Opps courier find : {order_courier['order_id']}")
                            list_orders_courier_to_calculate_unvavailable_time.append({
                                'courier_id': courier['_id']['courier_id'],
                                'order_id_first': order_courier['order_id'],
                                'start_order_first_time': order_courier['time_start'],
                                'end_order_first_time': order_courier['time_end'],
                                'order_id_second': courier['orders'][index_order+1]['order_id'],
                                'start_order_second_time': courier['orders'][index_order+1]['time_start'],
                                'end_order_second_time': courier['orders'][index_order+1]['time_end']
                            })
            
            final_list_times_unavailable = []    
            print(f'list_orders_courier_to_calculate_unvavailable_time = > {list_orders_courier_to_calculate_unvavailable_time}')            
            for order_int_list_unavailavle_time in list_orders_courier_to_calculate_unvavailable_time:
                order = 1
                all_couriers = 2
                order_time_from = None
                order_time_to = None
                for order_int_list_unavailavle_time_if_state in list_orders_courier_to_calculate_unvavailable_time:
                    if order_int_list_unavailavle_time['order_id_first'] != order_int_list_unavailavle_time_if_state['order_id_first'] and order_int_list_unavailavle_time['courier_id'] !=order_int_list_unavailavle_time_if_state['courier_id']:
                        # STEP 1 => Check if the month year day and hour is equal of start and end
                        if order_int_list_unavailavle_time['start_order_first_time'].day == order_int_list_unavailavle_time_if_state['start_order_first_time'].day and order_int_list_unavailavle_time['start_order_first_time'].year == order_int_list_unavailavle_time_if_state['start_order_first_time'].year and order_int_list_unavailavle_time['start_order_first_time'].month == order_int_list_unavailavle_time_if_state['start_order_first_time'].month and order_int_list_unavailavle_time['start_order_first_time'].hour == order_int_list_unavailavle_time_if_state['start_order_first_time'].hour:
                            #if order_int_list_unavailavle_time['end_order_first_time'].day == order_int_list_unavailavle_time_if_state['end_order_first_time'].day and order_int_list_unavailavle_time['end_order_first_time'].year == order_int_list_unavailavle_time_if_state['end_order_first_time'].year and order_int_list_unavailavle_time['end_order_first_time'].month == order_int_list_unavailavle_time_if_state['end_order_first_time'].month and order_int_list_unavailavle_time['end_order_first_time'].hour == order_int_list_unavailavle_time_if_state['end_order_first_time'].hour:
                            #    order = order + 1
                            if order_int_list_unavailavle_time['start_order_first_time'] < order_int_list_unavailavle_time_if_state['start_order_first_time'] :
                                order_time_from= order_int_list_unavailavle_time['start_order_first_time']
                            else:
                                order_time_from= order_int_list_unavailavle_time_if_state['start_order_first_time']
                                
                            if order_int_list_unavailavle_time['end_order_second_time']<order_int_list_unavailavle_time_if_state['end_order_second_time']:
                                order_time_to= order_int_list_unavailavle_time['end_order_second_time']
                            else:
                                order_time_to= order_int_list_unavailavle_time_if_state['end_order_second_time']
                            print('i am here')   
                        else:
                            if order_int_list_unavailavle_time['start_order_first_time']<order_int_list_unavailavle_time_if_state['start_order_first_time'] :
                                order_time_from= order_int_list_unavailavle_time_if_state['start_order_first_time']
                            else:
                                order_time_from= order_int_list_unavailavle_time['start_order_first_time']
                                
                            if order_int_list_unavailavle_time['end_order_second_time']<order_int_list_unavailavle_time_if_state['end_order_second_time']:
                                order_time_to= order_int_list_unavailavle_time_if_state['end_order_second_time']
                            else:
                                order_time_to= order_int_list_unavailavle_time['end_order_second_time']
                            print('i am here')
                if order_time_from is not None and order_time_to is not None:
                    if len(final_list_times_unavailable)>0:
                        alredy_exist = False
                        for list_time in final_list_times_unavailable:
                            if list_time['from'] == order_time_from.isoformat() and list_time['to'] == order_time_to.isoformat() :
                                alredy_exist = True
                                break
                        if alredy_exist != True:
                            final_list_times_unavailable.append(
                                {
                                    "from":order_time_from.isoformat(),
                                    "to":order_time_to.isoformat()
                                })
                    else:
                        final_list_times_unavailable.append(
                            {
                                "from":order_time_from.isoformat(),
                                "to":order_time_to.isoformat()
                            }
                        )
            print(final_list_times_unavailable)
            return final_list_times_unavailable
        except Exception as e:
            logging.error(e)
