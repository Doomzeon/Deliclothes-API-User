import requests
import json
import time
import logging
from bin.utils.database import Database
import bin.utils.logger as logger #import LogLevel, Logger

_logger = logger.Logger()

class Zara:

    def __init__(self):  # , language:str, city:str, cap:int):
        self.language = 'it'  # language
        self.city = 'city'
        self.cap = 'cap'

    def get_clothes(self, category_id: int, id_user:int =None) -> dict:
        try:
            products = self.get_products_by_gender_and_type(
                category_id=category_id)
           # print(products)
            return self.__convert_products(products=products, id_user=id_user)
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            

    def get_similar_clothes(self, product_id: int) -> dict:
        try:
            products = self.__get_similar_products(
                product_id=product_id)
            return self.__convert_similar_products(products=products['similars'])
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')

    def get_related_clothes(self, product_id: int) -> dict:
        try:
            products = self.__get_related_products(
                product_id=product_id)
            return self.__convert_similar_products(products=products['recommend'])
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')


    def __get_similar_products(self, product_id: int) -> dict:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}

            d = requests.get(
                f'https://www.zara.com/it/{self.language}/product/{product_id}/similar?ajax=true', headers=header).json()
            return d
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)

    def __get_related_products(self, product_id: id) -> dict:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}

            d = requests.get(
                f'https://www.zara.com/it/{self.language}/product/{product_id}/related?ajax=true', headers=header).json()
            return d
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)

    def __convert_similar_products(self, products: list) -> dict:
        try:
            clothes = []
            for product in products:
               # print(product)
                if product.get('availability') == 'in_stock':
                    product_detail = self.__get_product_info(
                        product_id=product['id'])
                    print(f"processing {product['id']} \n")
                    clothes.append({
                        'brand_name': 'Zara',
                        'id_product': product['id'],
                        'title': product_detail[0]['name'],
                        'type': 'test',
                        'description': product_detail[0]['description'],
                        'price': self.__convert_price(product_detail[0]['price']),
                        # => convert
                        'old_price': "product_detail[0].get('oldPrice')",
                        'discountPercentage': product_detail[0].get('displayDiscountPercentage'),
                        'care': product_detail[0]['detail'].get('care'),
                        'image_poster': f"https://static.zara.net/photos//{product_detail[0]['xmedia'][2]['path']}/w/1104/{product_detail[0]['xmedia'][2]['name']}.jpg?ts=1614673699842",
                        # => colors, sizes for each color
                        'colors': self.__get_colors(product_colors_body=product_detail[0]['detail'].get('colors')),
                        'images': self.__get_images(xmedia=product_detail[0]['xmedia']),
                        'sizes': self.__get_sizes_first_clothe(first_clothe=product_detail[0]['detail'].get('colors')),
                        'user_liked': False,
                        'size_selected':''
                    })
                #time.sleep(0.4)
                #print(len(clothes))
            return clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)


    def __convert_price(self, price: int) -> str:
        try:

            price = str(price)
            final_price = ''
            #print(price)
            #print(len(price))
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
            #print(final_price)
            return float(final_price)
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            

    def __convert_products(self, products: list, id_user:int=None) -> dict:
        try:
            #print(id_user)
            clothes = []
           # print(len(products['productGroups'][0]['elements']))
            filterred_arr_products = list(filter(lambda item: item.get('commercialComponents') and item['commercialComponents'][0].get(
                'availability') == 'in_stock', products['productGroups'][0]['elements']))
            splitted_arr = filterred_arr_products[:12]
            #print(len(splitted_arr))
            for product in splitted_arr:
                clothe_liked_by_user = False
                if id_user is not None:
                    clothe_liked_by_user = Database().check_clothe_if_is_liked(id_clothe= product['commercialComponents'][0]['id'], id_user= id_user)
                # if product.get('commercialComponents') and product['commercialComponents'][0].get('availability') == 'in_stock':
               # print(product['commercialComponents'][0]['id'])
                product_detail = self.__get_product_info(
                    product_id=product['commercialComponents'][0]['id'])
                #print(
                #    f"processing {product['commercialComponents'][0]['id']} \n")
               # print(f"Xmedia:=> {product_detail[0]['xmedia']}")
                clothes.append({
                    'brand_name': 'Zara',
                    'id_product': product['commercialComponents'][0]['id'],
                    'title': product_detail[0]['name'],
                    'type': 'test',
                    'description': product_detail[0]['description'],
                    'price': self.__convert_price(product_detail[0]['price']),
                    # => convert
                    'old_price': "product_detail[0].get('oldPrice')",
                    'discountPercentage': product_detail[0].get('displayDiscountPercentage'),
                    'care': product_detail[0]['detail'].get('care'),
                    'image_poster': f"https://static.zara.net/photos//{product_detail[0]['xmedia'][0]['path']}/w/1104/{product_detail[0]['xmedia'][0]['name']}.jpg?ts=1614673699842",
                    # => colors, sizes for each color
                    'colors': self.__get_colors(product_colors_body=product_detail[0]['detail'].get('colors')),
                    'images': self.__get_images(xmedia=product_detail[0]['xmedia']),
                    'sizes': self.__get_sizes_first_clothe(first_clothe=product_detail[0]['detail'].get('colors')),
                    #'id_sizes':self.__get_id_sizes_first_clothe(first_clothe=product_detail[0]['detail'].get('colors'))
                    'user_liked': clothe_liked_by_user,
                    'size_selected':''
                })
                time.sleep(0.4)
               # print(clothes[0])
            return clothes
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)
        

    def __get_sizes_first_clothe(self, first_clothe):
        try:
            sizes = []
          #  print(first_clothe[0]['sizes'])
            if first_clothe is not None:
                for size in first_clothe[0]['sizes']:
                    print(size)
                    sizes.append(size['name'])
            return sizes
        except Exception as e:
            pass
           # print(f'First sizes clothe: {e}')

    def __get_images(self, xmedia: list):
        try:
            final_list_images = []
            for media in xmedia:
                final_list_images.append(
                    f"https://static.zara.net/photos//{media['path']}/w/1104/{media['name']}.jpg?ts=1614673699842")
            return final_list_images
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            
            
    def __get_colors(self, product_colors_body: list) -> list:
        try:
            # print(product_colors_body)
            product_colors_info = []
            # print(product_colors_body)
            if product_colors_body:
                for color_info in product_colors_body:
                    # print(color_info)
                    product_colors_info.append(
                        {
                            'color_hex': color_info.get('hexCode'),
                            'image_posters': self.__conver_image_posters(posters_info=color_info.get('xmedia'))

                        }
                    )
            return product_colors_info
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            #raise(e)


    def __conver_image_posters(self, posters_info):
        try:
            posters = []
            if posters_info:
                for poster in posters_info:
                    posters.append(
                        f"https://static.zara.net/photos//{poster['path']}/w/1104/{poster['name']}.jpg?ts=1614673699842"
                    )
            return posters
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)
        

    def __get_product_info(self, product_id: int) -> list:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}

            d = requests.get(
                f'https://www.zara.com/it/{self.language}/products-details?productIds={product_id}&ajax=true', headers=header).json()
           # print(d)
            return d
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)
        

    def get_products_by_gender_and_type(self, category_id: int) -> list:
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}
            products = requests.get(
                f'https://www.zara.com/it/{self.language}/category/{category_id}/products?ajax=true', headers=header)
            # print(products)
            return products.json()
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
            raise(e)
    
    
    def get_product_availability(self, refer_id:int, lat:str, lng:str)->list:
        try:
            order = {
                'clothe_id':refer_id,
                'shops':[]
            }
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}
            shops = requests.get(
                f'https://www.zara.com/it/en/stores-locator/search?lat={lat}&lng={lng}&isGlobalSearch=false&showOnlyPickup=false&isDonationOnly=false&skipRestriction=true&includeFastSintInfo=false&ajax=true', headers=header)
            print('Get shops with success')
            #print(shops)
            for shop in shops.json():
                stocks = requests.get(f'https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/{refer_id}?physicalStoreId={shop["id"]}&ajax=true', headers=header).json()
                if len(stocks) > 0:
                    order['shops'].append({
                        'lat':shop['latitude'],
                        'lng':shop['longitude'],
                        'addressLines':shop['addressLines'],
                        "shop_id":shop['id'],
                        "clothes":[]
                    })
            return order
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')
    
    
    def directions_delivery(self, data_model:list)->list:
        try:
            same_shop = False
            
            shops_list = []
            for clothe in data_model:
                for shop in clothe['shops']:
                    if shop not in shops_list:
                        shops_list.append(shop)
                        
            for clothe in data_model:
                for shop_clothe in clothe['shops']:
                    for shop in shops_list:
                        if shop['lat'] == shop_clothe['lat'] and shop['lng'] == shop_clothe['lng'] and shop['shop_id'] == shop_clothe['shop_id']:
                            shop['clothes'].append(clothe['clothe_id'])
            shop_to_take_order = {}
            
            for shop_w_clothes in shops_list:
                if len(shop_w_clothes['clothes']) == len(data_model):
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
            
            
    def get_product_info_data(self, id_clothe:str, user_liked:bool=False):
        try:
            product_detail = self.__get_product_info(
                    product_id=id_clothe)
           # print(f"processing {id_clothe} \n")
            return {
                'brand_name': 'Zara',
                'id_product': int(id_clothe),
                'title': product_detail[0]['name'],
                'type': 'test',
                'description': product_detail[0]['description'],
                'price': self.__convert_price(product_detail[0]['price']),
                # => convert
                'old_price': "product_detail[0].get('oldPrice')",
                'discountPercentage': product_detail[0].get('displayDiscountPercentage'),
                'care': product_detail[0]['detail'].get('care'),
                'image_poster': f"https://static.zara.net/photos//{product_detail[0]['xmedia'][0]['path']}/w/1104/{product_detail[0]['xmedia'][0]['name']}.jpg?ts=1614673699842",
                'colors': self.__get_colors(product_colors_body=product_detail[0]['detail'].get('colors')),
                'images': self.__get_images(xmedia=product_detail[0]['xmedia']),
                'sizes': self.__get_sizes_first_clothe(first_clothe=product_detail[0]['detail'].get('colors')),
                'user_liked': user_liked,
                'size_selected':'S',
                'quantity':1
            }
        except Exception as e:
            _logger.log(e, logger.LogLevel.fatal, message=f'Exception occured while geeting products from zara')