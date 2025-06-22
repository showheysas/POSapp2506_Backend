from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class Transaction(Base):
    __tablename__ = 'transaction'

    TRD_ID = Column("trd_id", Integer, primary_key=True, index=True)
    DATETIME = Column("datetime", DateTime, default=datetime.utcnow)
    EMP_CD = Column("emp_cd", String(10))
    STORE_CD = Column("store_cd", String(5))
    POS_NO = Column("pos_no", String(3))
    TOTAL_AMT = Column("total_amt", Integer)
    TTL_AMT_EX_TAX = Column("ttl_amt_ex_tax", Integer)

    details = relationship("TransactionDetail", back_populates="transaction")


class TransactionDetail(Base):
    __tablename__ = 'transaction_detail'

    TRD_ID = Column("trd_id", Integer, ForeignKey("transaction.trd_id"), primary_key=True)
    DTL_ID = Column("dtl_id", Integer, primary_key=True)
    PRD_ID = Column("prd_id", Integer, nullable=True)
    PRD_CODE = Column("prd_code", BigInteger)  # ← CODEはint8型なのでBigInteger
    PRD_NAME = Column("prd_name", String(100))
    PRD_PRICE = Column("prd_price", Integer)
    TAX_CD = Column("tax_cd", String(2))

    transaction = relationship("Transaction", back_populates="details")
