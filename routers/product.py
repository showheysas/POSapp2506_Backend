from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.product_master import ProductMaster
from db import get_db

router = APIRouter()

@router.get("/items/{code}")
def get_product(code: int, db: Session = Depends(get_db)):
    try:
        product = db.query(ProductMaster).filter(ProductMaster.CODE == code).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # 明示的に辞書で返却（Pydanticを使わない）
        return {
            "code": product.CODE,
            "name": product.NAME,
            "price": product.PRICE,
        }
    except Exception as e:
        # ログストリームで追えるように出力
        print(f"[ERROR] /items/{code} の取得中にエラー発生: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
