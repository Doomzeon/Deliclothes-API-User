
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreditCardEntity(Base):
    __tablename__ = 'CREDIT_CARDS'

    id = Column(Integer, primary_key=True)
    id_stripe = Column(String)
    user_id = Column(Integer)
    title = Column(String)
    expiration_month = Column(Integer)
    expiration_year = Column(Integer)
    cvc = Column(Integer)
    card_number = Column(String)
    card_type = Column(String)

    