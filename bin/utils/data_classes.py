import datetime
from marshmallow_dataclass import dataclass

@dataclass
class CrediCard:
    title:str
    card_number:str
    expiration_month:int
    expiration_year:int
    cvc:int
    card_type:str
    owner:str=None
    id_stripe:str=None
    id:int = None
    
    
@dataclass
class Customer:
    email: str
    name: str
    surname: str
    residence: str
    phone_number:int
    country_code:str
    language:str
    zip_code:int
    gender:str
    id_city:int = 0
    country:str=None
    city:str=None
    id:int=None
    customer_id:str=None
    password: str=None
    credit_card: CrediCard= None
    

@dataclass
class User:
    email:str
    password:str
    
@dataclass
class ClotheLiked:
    id_clothe:str
    id_user:int
    brand:str
    
@dataclass
class ClotheDataBag:
    id_clothe:str
    brand:str
    id_user:int
    size:str
    quantity:int
    id_size:str
    returned:bool
    id: int=None
    
    
@dataclass
class Order:
    amount: int
    id_user:int
    hour_delivery: str
    day_delivery: str
    street_delivery: str
    credit_card_id: int
    clothes_dict: list 
    city:str
    zip_code:int
    directions:list
       
    
@dataclass
class UserInfo:
    name:str
    surname:str
    phone_number:str
    residence:str
    id_city:int
    
@dataclass
class PhoneDataScheleton:
    phone:int =None
    code: str = None
    
@dataclass
class UserMMDScheleton:
    id: int
    name:str = None
    surname:str = None
    residence: str = None
    phone: PhoneDataScheleton = None