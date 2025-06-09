from sqlalchemy import Column, Integer, String
from models import Base

class ProductMaster(Base):
    __tablename__ = 'product_master'

    PRD_ID = Column(Integer, primary_key=True)
    CODE = Column(Integer, unique=True, nullable=False)
    NAME = Column(String(50))
    PRICE = Column(Integer)