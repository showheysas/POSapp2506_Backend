from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.transaction import TransactionCreate, TransactionResult
from models.transaction import Transaction, TransactionDetail
from db import get_db
from datetime import datetime

router = APIRouter()

@router.post("/purchase", response_model=TransactionResult)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(
        DATETIME=datetime.utcnow(),
        EMP_CD=data.emp_cd,
        STORE_CD=data.store_cd,
        POS_NO=data.pos_no,
        TOTAL_AMT=0,
        TTL_AMT_EX_TAX=0
    )
    db.add(transaction)
    db.flush()

    total = 0
    total_ex = 0
    for i, item in enumerate(data.details):
        detail = TransactionDetail(
            TRD_ID=transaction.TRD_ID,
            DTL_ID=i + 1,
            PRD_ID=None,
            PRD_CODE=item.prd_code,
            PRD_NAME=item.prd_name,
            PRD_PRICE=item.prd_price,
            TAX_CD=item.tax_cd
        )
        total += item.prd_price
        total_ex += int(item.prd_price / 1.1)
        db.add(detail)

    transaction.TOTAL_AMT = total
    transaction.TTL_AMT_EX_TAX = total_ex
    db.commit()
    db.refresh(transaction)

    return TransactionResult(success=True, total_amount=total, total_amount_ex_tax=total_ex)
