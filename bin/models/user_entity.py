
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = 'USERS'

    id = Column(Integer, primary_key=True)
    email =Column(String)
    customer_id = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    phone_number = Column(Integer)
    country_code = Column(String)
    residence = Column(String)
    language = Column(String)
    active = Column(Boolean)
    zip_code = Column(Integer)
    city = Column(String)
    gender = Column(String)

    