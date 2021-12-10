
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClotheInTheBag(Base):
    __tablename__ = 'BAG'

    id=Column(Integer, primary_key=True)
    id_clothe = Column(String)
    id_user = Column(Integer)
    brand = Column(String)
    quantity = Column(Integer)
    size = Column(String)
    id_size = Column(String)

    