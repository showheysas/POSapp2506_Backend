from sqlalchemy import Column, Integer, BigInteger, String
from models import Base

class ProductMaster(Base):
    __tablename__ = 'product_master'

    PRD_ID = Column("prd_id", Integer, primary_key=True)
    CODE = Column("code", BigInteger, unique=True, nullable=False)
    NAME = Column("name", String(100))
    PRICE = Column("price", Integer)
