import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.product_master import ProductMaster
from db import get_db

router = APIRouter()
logger = logging.getLogger("uvicorn.error")  # ← Azureで確実に表示されるロガー

@router.get("/items/{code}")
def get_product(code: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductMaster).filter(ProductMaster.CODE == code).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        logger.info(f"取得した商品: CODE={product.CODE}, NAME={product.NAME}, PRICE={product.PRICE}")

        return {
            "code": product.CODE,
            "name": product.NAME,
            "price": product.PRICE,
        }

    except Exception as e:
        logger.exception(f"/items/{code} の取得中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
