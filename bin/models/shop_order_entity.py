

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()

class ShopOrder(Base):
    __tablename__ = 'SHOPS_ORDERS'

    id=Column(Integer, primary_key=True)
    idShop= Column(Integer)
    idOrder= Column(Integer)
    clothes = Column(JSON)
    prepare_to = Column(TIMESTAMP)

    