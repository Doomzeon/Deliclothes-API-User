
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shop(Base):
    __tablename__ = 'SHOPS'

    id=Column(Integer, primary_key=True)
    username= Column(String)
    password= Column(String)
    street = Column(String)
    city = Column(String)
    brand = Column(String)
    zip_code = Column(Integer)

    