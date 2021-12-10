import requests
import json
import time
import logging
from sqlalchemy.sql.functions import user

from sqlalchemy.sql.selectable import FromClause
from bin.services.database_new import Database
import bin.utils.logger as logger  # import LogLevel, Logger

_logger = logger.Logger()
_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}


class Zara:

    def __init__(self, language):
        self.language = language
        self.city = 'city'
        self.cap = 'cap'

    def get_clothes(self, category_id: int, id_user: int = None):
        try:
            logging.info(
                f'Making request to zara to get clothes of category {category_id}....')
            products = self.get_products_by_category(category_id=category_id)
            return self.__convert_products(products=products, id_user=id_user)
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while selecting clothes from zara')
            raise(e)

    def get_similar_clothes(self, product_id: int, id_user:int = None):
        try:
            logging.info(
                f'Making request to zara to get similar clothes of product id {product_id}....')
            products = requests.get(
                f'https://www.zara.com/it/{self.language}/product/{product_id}/similar?ajax=true', headers=_header).json()
            return self.__convert_similar_products(products=products['similars'])
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while selecting similar clothes from zara')

    def get_related_clothes(self, product_id: int, id_user:int = None) -> dict:
        try:
            logging.info(
                f'Making request to zara to get recomended clothes by product id {product_id}....')
            products = requests.get(
                f'https://www.zara.com/it/{self.language}/product/{product_id}/related?ajax=true', headers=_header).json()
            
            return self.__convert_similar_products(products=products['recommend'])
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while selecting related clothes from zara')

    def get_products_by_category(self, category_id: int):
        try:
            products = requests.get(
                f'https://www.zara.com/it/{self.language}/category/{category_id}/products?ajax=true', headers=_header)
            return products.json()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while selecting products from zara by category id: {category_id}')
            raise(e)

    def __get_clothe_info(self, product_id: int) -> list:
        try:
            d = requests.get(
                f'https://www.zara.com/it/{self.language}/products-details?productIds={product_id}&ajax=true', headers=_header).json()
            return d
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while get clothe info from zara')
            raise(e)
        
        
    def get_clothe_poster(self, id_clothe:str, user_liked: bool= False, id_user:int=None):
        try:
            logging.info(f'Trying to get clothe info of product with id {id_clothe}')
            clothe_datail = self.__get_clothe_info(product_id= id_clothe)
            return {
                'brand':'Zara',
                'id':str(id_clothe),
                'title': clothe_datail[0]['name'],
                'price': self.__convert_price(clothe_datail[0]['detail']['colors'][0]['price']),
                'discountPercentage': clothe_datail[0].get('displayDiscountPercentage'),
                'liked':user_liked,
                'size':'s',
                'old_price': self.__convert_price(clothe_datail[0]['detail']['colors'][0].get('oldPrice')),
                'img': self.get_plain_image(xmedias= clothe_datail[0]['detail']['colors'][0]['xmedia'])#f"https://static.zara.net/photos//{clothe_datail[0]['detail']['colors'][0]['xmedia'][1]['path']}/w/1104/{clothe_datail[0]['detail']['colors'][0]['xmedia'][1]['name']}.jpg?ts=1614673699842"
            }
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geeting products from zara')
            
            
    def get_plain_image(self, xmedias:list):
        try:
            logging.info(F'Trying to get plain image of {xmedias}')
            for xmedia in xmedias:
                if xmedia['kind'] == 'plain':
                    return f"https://static.zara.net/photos//{xmedia['path']}/w/1104/{xmedia['name']}.jpg?ts=1614673699842"
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geting plain image of clothe')
            raise(e)
        

    def get_product_info_data(self, id_clothe: str, user_liked: bool = False, id_user:int=None):
        try:
            logging.info(f'Trying to get clothe info...')
            product_detail = self.__get_clothe_info(
                product_id=id_clothe)
            logging.info(f'Selected with success product info {product_detail}')
            
            if type(id_user) is int:
                logging.info(f'Checking if clothe is liked by the user...')
                user_liked =  Database().is_clothe_liked(id_user=id_user, id_clothe=id_clothe)
            return {
                'brand_name': 'Zara',
                'id_product': int(id_clothe),
                'title': product_detail[0]['name'],
                'type': 'test',
                'description': product_detail[0]['detail']['colors'][0]['description'],
                'price': self.__convert_price(product_detail[0]['detail']['colors'][0]['price']),
                'old_price': "product_detail[0].get('oldPrice')",
                'discountPercentage': product_detail[0].get('displayDiscountPercentage'),
                'care': product_detail[0]['detail'].get('care'),
                'image_poster': self.get_plain_image(xmedias= product_detail[0]['detail']['colors'][0]['xmedia']),#f"https://static.zara.net/photos//{product_detail[0]['detail']['colors'][0]['xmedia'][0]['path']}/w/1104/{product_detail[0]['detail']['colors'][0]['xmedia'][0]['name']}.jpg?ts=1614673699842",
                'colors': self.__get_colors(product_colors_body=product_detail[0]['detail'].get('colors')),
                'images': self.__get_images(xmedia=product_detail[0]['detail']['colors'][0]['xmedia']),
                'sizes': self.__get_sizes_first_clothe(first_clothe=product_detail[0]['detail'].get('colors')),
                'user_liked': user_liked,
                'size_selected': 'S',
                'quantity': 1
            }
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geeting product info from zara')

    def __convert_products(self, products, id_user: int=None):
        try:
            clothes = []
            logging.info(f'Trying to convert products from zara=> {products}')
            if products.get('productGroups') is not None:
                filterred_arr_products = list(filter(lambda item: item.get('commercialComponents') and item['commercialComponents'][0].get(
                    'availability') == 'in_stock', products['productGroups'][0]['elements']))
                products = filterred_arr_products[:12]

            for product in products:
                clothe_liked_by_user = False
                if type(id_user) is int:
                    logging.info(F'Trying to check if clothe is liked by the user....')
                    clothe_liked_by_user =  Database().is_clothe_liked(id_user=id_user, id_clothe=product['commercialComponents'][0]['id'])

                #product_detail = self.__get_clothe_info(
                 #   product_id=product['commercialComponents'][0]['id'])
                logging.info(f'Trying to get clothe poster...')
                res = self.get_clothe_poster(id_clothe=product['commercialComponents'][0]['id'], user_liked=clothe_liked_by_user)
                clothes.append(res)
                time.sleep(0.4)
            logging.info(F'Clothes posters are: {clothes}')
            return clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while converting products from zara')
            raise(e)


    def __convert_similar_products(self, products: list, id_user:int=None) -> dict:
        try:
            logging.info(f'Trying to beautify similar/recomended products JSON data get in response')
            clothes = []
            for product in products:
                if product.get('availability') == 'in_stock':
                    logging.info(f'Geting clothe info with product id {product["id"]}')
                    product_detail = self.__get_clothe_info(
                        product_id=product['id'])
                    liked = False
                    if id_user is not None:
                        logging.info(f'Checking if clothe is liked already by the user')
                        liked = Database().is_clothe_liked(id_user=id_user, id_clothe=product['id'])
                    clothes.append({
                        'brand': 'Zara',
                        'id': str(product['id']),
                        'title': product_detail[0]['name'],
                        'price': self.__convert_price(product_detail[0]['detail']['colors'][0]['price']),
                        'discountPercentage': product_detail[0].get('displayDiscountPercentage'),
                        'img': self.get_plain_image(xmedias= product_detail[0]['detail']['colors'][0]['xmedia']),#f"https://static.zara.net/photos//{product_detail[0]['detail']['colors'][0]['xmedia'][0]['path']}/w/1104/{product_detail[0]['detail']['colors'][0]['xmedia'][0]['name']}.jpg?ts=1614673699842",
                        'liked': liked
                    })
            return clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while converting similar/recomended clothes from zara')
            raise(e)

    def __get_sizes_first_clothe(self, first_clothe):
        try:
            sizes = []
            logging.info(f'Trying to get first size of clothe {first_clothe}')
            if first_clothe is not None:
                for size in first_clothe[0]['sizes']:
                    sizes.append(size['name'])
            return sizes
        except Exception as e:
            pass

    def __conver_image_posters(self, posters_info):
        try:
            posters = []
            logging.info(F'Trying to convert image posters {posters_info}....')
            if posters_info:
                for poster in posters_info:
                    posters.append(
                        f"https://static.zara.net/photos//{poster['path']}/w/1104/{poster['name']}.jpg?ts=1614673699842"
                    )
            return posters
        except Exception as e:
            raise(e)

    def get_product_availability(self, refer_id: int, lat: str, lng: str) -> list:
        try:
            logging.info(f'Trying to get product availability {refer_id}....')
            order = {
                'clothe_id': refer_id,
                'shops': []
            }
            logging.info(f'Searching for the shops....')
            shops = requests.get(
                f'https://www.zara.com/it/en/stores-locator/search?lat={lat}&lng={lng}&isGlobalSearch=false&showOnlyPickup=false&isDonationOnly=false&skipRestriction=true&includeFastSintInfo=false&ajax=true', headers=_header)
            logging.info(F'Found shops: {shops}')
            logging.info(f'Checking if shops have in stock clothe....')
            for shop in shops.json():
                stocks = requests.get(
                    f'https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/{refer_id}?physicalStoreId={shop["id"]}&ajax=true', headers=_header).json()
                if len(stocks) > 0:
                    order['shops'].append({
                        'lat': shop['latitude'],
                        'lng': shop['longitude'],
                        'addressLines': shop['addressLines'],
                        "shop_id": shop['id'],
                        "clothes": []
                    })
            logging.info('Procceced product availability final object: {order}')
            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geeting products availability zara')

    def __get_colors(self, product_colors_body: list) -> list:
        try:
            logging.info(f'Trying to get colors of clothe....')
            product_colors_info = []
            if product_colors_body:
                for color_info in product_colors_body:
                    product_colors_info.append(
                        {
                            'color_hex': color_info.get('hexCode'),
                            'image_posters': self.__conver_image_posters(posters_info=color_info.get('xmedia'))

                        }
                    )
            return product_colors_info
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while proccesing colors of clothe from zara')
            raise(e)

    def __get_images(self, xmedia: list):
        try:
            logging.info(f'Trying to get images of clothe {xmedia}...')
            final_list_images = []
            for media in xmedia:
                final_list_images.append(
                    f"https://static.zara.net/photos//{media['path']}/w/1104/{media['name']}.jpg?ts=1614673699842")
            return final_list_images
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geting images of clothe from zara')

    def __convert_price(self, price: int) -> str:
        try:
            logging.info(F'Trying to convert price of clothe {price}...')
            if price:
                price = str(price)
                final_price = ''
                for p in price:
                    if len(price) == 3:
                        if len(final_price) == 1:
                            final_price += '.'+p
                        elif len(final_price) == 3 or len(final_price) == 0:
                            final_price += p
                    if len(price) == 4:
                        if len(final_price) == 2:
                            final_price += '.'+p
                        elif len(final_price) == 4 or len(final_price) == 0 or len(final_price) == 1:
                            final_price += p
                return float(final_price)
            else:
                return 0.0
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while converting price of clothe from zara')
            
    def get_refer_id_of_the_clothe_by_size(self, id_clothe, selected_size:str):
        try:
            logging.info(f'Trying to get refere id of clothe by size {selected_size}')
            
            clothe_data = self.__get_clothe_info(product_id= id_clothe)
            for size in clothe_data[0]['detail']['colors'][0]['sizes']:
                if size['name'].lower() == selected_size.lower():
                    size_reference_splitted = size['reference'].split('-')
                    logging.info(f'Founded referer id of clothe : {size_reference_splitted[0][:-2]}')
                    return size_reference_splitted[0][:-2], size['id']
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geting referere id size of clothe from zara')
            
    def get_product_availability_in_shops(self, reference_id_product_without_id_size, id_size):
        try:
            url = f"https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/I2021/product/part-number/{reference_id_product_without_id_size}?physicalStoreId=3307,3197,9720,9105,3327,3530,12859,9123,3529,3391,3198,6437,3399&ajax=true"
            shops_ids = []
            logging.info('Contacting Zara to find clothe availability')
            response_shops = requests.get(url,  headers=_header)
            logging.info(f'Finding shops that have product with the size id {id_size}')
            logging.info(f'response_shops.json() = {response_shops.json()}')
            for shop in response_shops.json()['stocks']:
                print(shop)
                for size in shop['sizeStocks']:
                    if size['sizeId']== id_size:
                        shops_ids.append({
                            "shop_id":shop['physicalStoreId']
                        })
            logging.info(f'Found clothes inside the shops => {shops_ids}')
            return shops_ids
                
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geting products availability of clothe from zara')
            
            ####
    
    
            
            
    def directions_delivery(self, clothe_list:list):
        try:
            
            same_shop = False
            
            shops_list = []
            for clothe in clothe_list:
                for shop in clothe['shops']:
                    if shop not in shops_list:
                        shops_list.append(shop)
                        
            for clothe in clothe_list:
                for shop_clothe in clothe['shops']:
                    for shop in shops_list:
                        if shop['lat'] == shop_clothe['lat'] and shop['lng'] == shop_clothe['lng'] and shop['shop_id'] == shop_clothe['shop_id']:
                            shop['clothes'].append(clothe['clothe_id'])
            shop_to_take_order = {}
            
            for shop_w_clothes in shops_list:
                if len(shop_w_clothes['clothes']) == len(clothe_list):
                    same_shop = True
                    shop_to_take_order = shop_w_clothes
                    break
            if same_shop == True:
               # print(shop_to_take_order)
                return shop_to_take_order
            else:    
                for shop in shops_list:
                    if len(shop['clothes'])>1:
                        for over_shops in shops_list:
                            if shop != over_shops and len(over_shops['clothes'])<=1:
                                for clothe_id in shop['clothes']:
                                    if clothe_id in over_shops['clothes']:
                                        
                                        over_shops['clothes'].pop(over_shops['clothes'].index(clothe_id))
                                        
                new_shop_list = []
                shop_list_ids = []            
                for shop in shops_list:
                    if len(shop['clothes'])!=0:
                        new_shop_list.append(shop)
                        shop_list_ids.append(shop['shop_id'])
                        #shops_list.pop(shops_list.index(shop))
                        
                        
                for id_shop in shop_list_ids:
                    filtered_arr = list(filter(lambda item: item['shop_id']==id_shop, new_shop_list))
                    #print(filtered_arr)
                    duplicates_clothes_ids = list(filter(lambda item: item['clothes'] == filtered_arr[0]['clothes'], new_shop_list))
                    #print(duplicates_clothes_ids)
                    if len(duplicates_clothes_ids)>1:
                      #  print('trovato')
                      #  print(duplicates_clothes_ids)
                        new_shop_list.remove(duplicates_clothes_ids[0])
                return new_shop_list       
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal,
                        message=f'Exception occured while geeting products from zara')
            raise(e)
        
        
