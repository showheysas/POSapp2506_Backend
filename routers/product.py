from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from models.product_master import ProductMaster
from schemas.product_master import ProductOut
from db import get_db  # DB接続ヘルパー

# ログの設定
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/items/{code}", response_model=ProductOut)
def get_product(code: int, db: Session = Depends(get_db)):
    try:
        logging.info(f"Looking up product with code: {code}")
        product = db.query(ProductMaster).filter(ProductMaster.CODE == code).first()
        if not product:
            logging.warning(f"Product not found: {code}")
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        logging.exception("Error occurred while retrieving product")
        raise HTTPException(status_code=500, detail=str(e))
