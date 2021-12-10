
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClothesLiked(Base):
    __tablename__ = 'LIKED_CLOTHES'

    id = Column(Integer, primary_key=True)
    id_clothe = Column(String)
    id_user = Column(Integer)
    brand = Column(String)

    