
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()

class OrderEntity(Base):
    __tablename__ = 'ORDERS'

    id_user = Column(Integer)
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer)
    clothes = Column(MutableList.as_mutable(JSON))
    hour_delivery =Column(String)
    day_delivery =Column(String)
    status =Column(String)
    street_delivery = Column(String)
    credit_card_id = Column(Integer)
    stripe_id_intent = Column(String)
    amount = Column(String)
    city = Column(String)
    zip_code = Column(Integer)
    delivery_start_time= Column(String)
    directions= Column(MutableList.as_mutable(JSON))
    start = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    status_int = Column(Integer)
    

    