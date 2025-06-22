from pydantic import BaseModel, Field
from typing import List

# 商品明細（入力専用）
class TransactionDetailCreate(BaseModel):
    prd_code: int  # ← 修正
    prd_name: str
    prd_price: int
    tax_cd: str
    quantity: int  # ★ 追加

# 取引全体（入力専用）
class TransactionCreate(BaseModel):
    emp_cd: str
    store_cd: str
    pos_no: str
    details: List[TransactionDetailCreate] = Field(..., min_items=1)

# レスポンス用
class TransactionResult(BaseModel):
    success: bool
    total_amount: int
    total_amount_ex_tax: int

    class Config:
        from_attributes = True  # Pydantic v2 以降の orm_mode 相当
