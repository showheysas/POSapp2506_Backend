from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.product_master import ProductMaster
from schemas.product_master import ProductOut
from db import get_db

router = APIRouter()

@router.get("/items/{code}", response_model=ProductOut)
def get_product(code: int, db: Session = Depends(get_db)):
    # codeはintでもBigIntegerにもマッチする（SQLAlchemy側で吸収される）
    product = db.query(ProductMaster).filter(ProductMaster.CODE == code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
