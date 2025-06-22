from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.transaction import TransactionCreate, TransactionResult
from models.transaction import Transaction, TransactionDetail
from models.product_master import ProductMaster
from db import get_db
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/purchase", response_model=TransactionResult)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = Transaction(
        DATETIME=datetime.utcnow() + timedelta(hours=9),
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
    detail_id = 1

    for item in data.details:
        print(f"Received item: {item}")
        product = db.query(ProductMaster).filter(ProductMaster.CODE == int(item.prd_code)).first()
        
        if not product:
            print("Product not found in DB")
            raise HTTPException(status_code=400, detail="Product not found")

        if product.NAME != item.prd_name or product.PRICE != item.prd_price:
            print(f"Mismatch - DB: {product.NAME}, {product.PRICE} | Input: {item.prd_name}, {item.prd_price}")
            raise HTTPException(status_code=400, detail="Product info mismatch")

        for _ in range(item.quantity):
            detail = TransactionDetail(
                TRD_ID=transaction.TRD_ID,
                DTL_ID=detail_id,
                PRD_ID=product.PRD_ID,
                PRD_CODE=item.prd_code,
                PRD_NAME=item.prd_name,
                PRD_PRICE=item.prd_price,
                TAX_CD=item.tax_cd
            )
            db.add(detail)
            total += item.prd_price
            total_ex += int(item.prd_price / 1.1)
            detail_id += 1

    transaction.TOTAL_AMT = total
    transaction.TTL_AMT_EX_TAX = total_ex
    db.commit()
    db.refresh(transaction)

    print("Returning transaction result:", total, total_ex)
    return TransactionResult(success=True, total_amount=total, total_amount_ex_tax=total_ex)
