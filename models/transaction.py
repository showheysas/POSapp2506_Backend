from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from models import Base

class Transaction(Base):
    __tablename__ = 'transaction'

    TRD_ID = Column(Integer, primary_key=True, index=True)

    # 日本時間で記録されるように修正
    DATETIME = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=9))))

    EMP_CD = Column(String(10))
    STORE_CD = Column(String(5))
    POS_NO = Column(String(3))
    TOTAL_AMT = Column(Integer)
    TTL_AMT_EX_TAX = Column(Integer)

    details = relationship("TransactionDetail", back_populates="transaction")



class TransactionDetail(Base):
    __tablename__ = 'transaction_detail'

    TRD_ID = Column(Integer, ForeignKey("transaction.TRD_ID"), primary_key=True)
    DTL_ID = Column(Integer, primary_key=True)
    PRD_ID = Column(Integer, nullable=True)  # ← ここをnullableに
    PRD_CODE = Column(String(13))
    PRD_NAME = Column(String(50))
    PRD_PRICE = Column(Integer)
    TAX_CD = Column(String(2))

    transaction = relationship("Transaction", back_populates="details")
