from flask import Response
import json
from bin.services.zara import Zara



woman_zara = [
    {
        "category_id":1718095,
        "type_name":'Jackets',
        "gender":'Woman'
    },
    {
        "category_id":1882227,
        "type_name":'Blazers',
        "gender":'Woman'
    },
    {
        "category_id":1718088,
        "type_name":'Waiskots',
        "gender":'Woman'
    },
    {
        "category_id":1718163,
        "type_name":'Dresses',
        "gender":'Woman'
    },
    {
        "category_id":1718198,
        "type_name":'Knitwear',
        "gender":'Woman'
    },
    {
        "category_id":1718817,
        "type_name":'T-shirt',
        "gender":'Woman'
    },
    {
        "category_id":1718862,
        "type_name":'Sweaters',
        "gender":'Woman'
    },
    {
        "category_id":1718780,
        "type_name":'Jeans',
        "gender":'Woman'
    },
    {
        "category_id":1718736,
        "type_name":'Trousers',
        "gender":'Woman'
    },
    {
        "category_id":1718879,
        "type_name":'Shorts',
        "gender":'Woman'
    },
    {
        "category_id":1718788,
        "type_name":'Skirt',
        "gender":'Woman'
    },
    {
        "category_id":1718183,
        "type_name":'Shirts-tops',
        "gender":'Woman'
    },
    {
        "category_id":1719457,
        "type_name":'Loungewear',
        "gender":'Woman'
    },
    {
        "category_id":1719408,
        "type_name":'Suits',
        "gender":'Woman'
    },
    {
        "category_id":1719442,
        "type_name":'Seamless',
        "gender":'Woman'
    },
    {
        "category_id":1718981,
        "type_name":'Shoes',
        "gender":'Woman'
    },
    {
        "category_id":1719123,
        "type_name":'Bags',
        "gender":'Woman'
    },
    {
        "category_id":1719379,
        "type_name":'Accessories',
        "gender":'Woman'
    },
    {
        "category_id":1750767,
        "type_name":'SpecialPrice',
        "gender":'Woman'
    },
    {
        "category_id":1719404,
        "type_name":'Lingerie',
        "gender":'Woman'
    },
    {
        "category_id":1717639,
        "type_name":'Jackets',
        "gender":'Man'
    },
    {
        "category_id":1717679,
        "type_name":'Overshirts',
        "gender":'Man'
    },
    {
        "category_id":1717677,
        "type_name":'Blazer',
        "gender":'Man'
    },
    {
        "category_id":1717658,
        "type_name":'Waiskots',
        "gender":'Man'
    },
    {
        "category_id":1720409,
        "type_name":'Loungewear', 
        "gender":'Man'
    },
    {
        "category_id":1720315,
        "type_name":'Shirts-tops',
        "gender":'Man'
    },
    {
        "category_id":1720373,
        "type_name":'Maglietta',
        "gender":'Man'
    },
    {
        "category_id":1720387,
        "type_name":'Polo',
        "gender":'Man'
    },
    {
        "category_id":1717716,
        "type_name":'Sweaters',
        "gender":'Man'
    },
    {
        "category_id":1720321,
        "type_name":'Sportswear',
        "gender":'Man'
    },
    {
        "category_id":1720273,
        "type_name":'Jeans',
        "gender":'Man'
    },
    {
        "category_id":1720241,
        "type_name":'Pantaloni',
        "gender":'Man'
    },
    {
        "category_id":1717689,
        "type_name":'Dresses',
        "gender":'Man'
    },
    {
        "category_id":1720413,
        "type_name":'Shoes',
        "gender":'Man'
    },
    {
        "category_id":1720458,
        "type_name":'Bags',
        "gender":'Man'
    },
    {
        "category_id":1720640,
        "type_name":'SpecialPrice',
        "gender":'Man'
    }
    
]

class ClothesController:
    def __init__(self, offset: int, size: int):
        self._offset = offset
        self._size = size

    def get_home_page_posters(self) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            #database = Database()
            #posters = database.select_posters()
            #if posters == None or len(posters) == 0:
            #    raise(Exception('There is no data inside DB'))
            print('RESposne')
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "Selected with success posters from DB",
                        "payload": json.dumps(
                            [{
                                "brand": "Zara",
                                "description": "Fino a 60% \nsui vestiti di Zara",
                                "imagePoster": "assets/images/home_1.jpeg",
                                
                            },{
                                "brand": "Zara",
                                "description": "New in \nof clothes from Zara",
                                "imagePoster": "assets/images/home_2.jpeg",
                                
                            }
                            ]
                            )
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
                        "message": "Internal server error. During handaling of 'get_home_page_posters' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_clothes_info(self, type_clothes: str, gender: str, id_user:int = None) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            zara_dict = list(filter(lambda item: item['gender'].lower() == gender.lower() and item['type_name'].lower() == type_clothes.lower(), woman_zara))
            print(zara_dict)
            zara = Zara(language='en')
            zara_clothes = zara.get_clothes(category_id= zara_dict[0]['category_id'], id_user=id_user)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload":json.dumps(zara_clothes)
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
                        "message": "Internal server error. During handaling of 'get_clothes_by_gender_and_type' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_clothes_similar(self, product_id: int) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            zara = Zara()
            zara_clothes = zara.get_similar_clothes(product_id=product_id)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload":json.dumps(zara_clothes)
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
                        "message": "Internal server error. During handaling of 'get_clothes_by_gender_and_type' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_clothes_recomended(self, product_id: int) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            zara = Zara()
            zara_clothes = zara.get_related_clothes(product_id=product_id)
            return Response(
                json.dumps(
                    {
                        "status": 200,
                        "message": "OK",
                        "payload":json.dumps(zara_clothes)
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
                        "message": "Internal server error. During handaling of 'get_clothes_by_gender_and_type' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def get_clothes_liked_by_user(self, username: str) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            #database = Database()
            #clothes = database.select_liked_clothes(username=username)

            #if clothes == None or len(clothes) == 0:
             #   raise(Exception('There is no data inside DB'))

            return Response(
                
                json.dumps(
                    {
                        "status": 200,
                        "message": "Selected with success clothes from DB",
                        "payload": json.dumps(
                            [{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            },{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            },{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            },{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            },{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            },{
                                "title": "T-SHIRT BASIC SCOLLO A V",
                                "description": "JOIN LIFE Care for fiber: 100 % cotone organico. Cotone coltivato utilizzando fertilizzanti e pesticidi naturali Inoltre, nella sua coltivazione non vengono utilizzate sementi  geneticamente modificate, aiu",
                                "imagePoster": "assets/images/t-shirt-1.jpg",
                                "brand": "Zara",
                                "price": 17.99,
                                "type": "New In",
                                "liked": True,
                                "sizes": [
                                    "s",
                                    "l"
                                ]
                            }]
                        
                        
                        )
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
                        "message": "Internal server error. During handaling of 'get_clothes_liked_by_username' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def like_clothe_by_user(self, username: str, clothe_title: str) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            database = Database()
            database.like_clothe(username=username, clothe_title=clothe_title)

            return Response(
                json.dumps(
                    {
                        "status": 201,
                        "message": "Added with success liked clothe by user",
                        "payload": json.dumps(clothes)
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
                        "message": "Internal server error. During handaling of 'like_clothe_by_user' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )

    def dislike_clothe_by_user(self, username: str, clothe_title: str) -> Response:
        """ Buisness logic of clohtes controller  """
        try:
            database = Database()
            database.dislike_clothe(
                username=username, clothe_title=clothe_title)

            return Response(
                json.dumps(
                    {
                        "status": 201,
                        "message": "Added with success liked clothe by user",
                        "payload": json.dumps(clothes)
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
                        "message": "Internal server error. During handaling of 'like_clothe_by_user' an errore occured"
                    }
                ),
                status=500,
                mimetype="application/json"
            )


# TODO: add logging instead of print
# TODO: add to the Database object in the future connection
# TODO: add fake JSON data inside response


