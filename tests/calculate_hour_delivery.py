import unittest

data_set_with_different_shops = [
    {
        "clothe_id":1,
        "shops":[
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":8
            },
            {
                'clothes':[],
                "lat":8,
                "lng":3,
                "shop_id":9
            }
        ]
    },
    {
        "clothe_id":2,
        "shops":[
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":8
            },
            {
                'clothes':[],
                "lat":28,
                "lng":23,
                "shop_id":11
            }
        ]
    },
    {
        "clothe_id":3,
        "shops":[
            {
                'clothes':[],
                "lat":32,
                "lng":15,
                "shop_id":12
            },
            {
                'clothes':[],
                "lat":32,
                "lng":1,
                "shop_id":13
            }
        ]
    },
    {
        "clothe_id":4,
        "shops":[
            {
                'clothes':[],
                "lat":4,
                "lng":3,
                "shop_id":14
            },
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":8
            }
        ]
    },
]

data_set_with_same_shop = [
    {
        "clothe_id":1,
        "shops":[
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":10
            },
            {
                'clothes':[],
                "lat":8,
                "lng":3,
                "shop_id":14
            }
        ]
    },
    {
        "clothe_id":2,
        "shops":[
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":10
            },
            {
                'clothes':[],
                "lat":28,
                "lng":23,
                "shop_id":24
            }
        ]
    },
    {
        "clothe_id":3,
        "shops":[
            {
                'clothes':[],
                "lat":12,
                "lng":15,
                "shop_id":10
            },
            {
                'clothes':[],
                "lat":28,
                "lng":23,
                "shop_id":24
            }
        ]
    }
]

from itertools import permutations, combinations
from collections import Counter
import numpy as np
class TestSum(unittest.TestCase):
    
    def test_same_shop(self):
        same_shop=False
        shops_list = []
        for clothe in data_set_with_same_shop:
            for shop in clothe['shops']:
                if shop not in shops_list:
                    shops_list.append(shop)
                    
        for clothe in data_set_with_same_shop:
            for shop_clothe in clothe['shops']:
                for shop in shops_list:
                    if shop['lat'] == shop_clothe['lat'] and shop['lng'] == shop_clothe['lng'] and shop['shop_id'] == shop_clothe['shop_id']:
                        shop['clothes'].append(clothe['clothe_id'])
        shop_to_take_order = {}
        
        for shop_w_clothes in shops_list:
            if len(shop_w_clothes['clothes']) == len(data_set_with_same_shop):
                same_shop = True
                shop_to_take_order = shop_w_clothes
                break
        
                        
        #print(shop_to_take_order)
        #print(np.unique(new_per_list))
        self.assertEqual(same_shop, True, "Should be true")

    def test_different_shop(self):
        print('Test n2 => \n\n\n\n\n\n')
        same_shop=False
        
        shops_list = []
        for clothe in data_set_with_different_shops:
            for shop in clothe['shops']:
                if shop not in shops_list:
                    shops_list.append(shop)
                    
        for clothe in data_set_with_different_shops:
            for shop_clothe in clothe['shops']:
                for shop in shops_list:
                    if shop['lat'] == shop_clothe['lat'] and shop['lng'] == shop_clothe['lng'] and shop['shop_id'] == shop_clothe['shop_id']:
                        shop['clothes'].append(clothe['clothe_id'])
        shop_to_take_order = {}
        
        for shop_w_clothes in shops_list:
            if len(shop_w_clothes['clothes']) == len(data_set_with_different_shops):
                same_shop = True
                shop_to_take_order = shop_w_clothes
                break
        if same_shop == False:    
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
                    print('trovato')
                    print(duplicates_clothes_ids)
                    new_shop_list.remove(duplicates_clothes_ids[0])
                
            print(new_shop_list)    
        self.assertEqual(same_shop, False, "Should be true")
            

if __name__ == '__main__':
    unittest.main()