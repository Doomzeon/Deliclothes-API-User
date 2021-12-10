
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()

class PostersEntity(Base):
    __tablename__ = 'POSTERS'

    id = Column(Integer, primary_key=True)
    brand = Column(String)
    description = Column(String)
    image_poster =Column(String)
    #callback = Column(String)
    