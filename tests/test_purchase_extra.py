import pytest
from schemas.transaction import TransactionCreate, TransactionDetailCreate

def test_create_transaction_product_not_found(client):
    payload = {
        "emp_cd": "9999999999",
        "store_cd": "00030",
        "pos_no": "090",
        "details": [
            {
                "prd_code": "9999999999999",  # 存在しないコード
                "prd_name": "存在しない商品",
                "prd_price": 999,
                "tax_cd": "01",
                "quantity": 1
            }
        ]
    }
    response = client.post("/purchase", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product not found"

def test_create_transaction_product_mismatch(client, test_db):
    payload = {
        "emp_cd": "9999999999",
        "store_cd": "00030",
        "pos_no": "090",
        "details": [
            {
                "prd_code": "4901480151908",
                "prd_name": "名前違い",  # 登録と異なる名前
                "prd_price": 999,       # 登録と異なる価格
                "tax_cd": "01",
                "quantity": 1
            }
        ]
    }
    response = client.post("/purchase", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Product info mismatch"

def test_create_transaction_with_negative_price(client):
    data = TransactionCreate(
        emp_cd="E003",
        store_cd="S003",
        pos_no="03",
        details=[
            TransactionDetailCreate(
                prd_code="4901480151908",
                prd_name="テスト商品",
                prd_price=-100,  # マイナス価格
                tax_cd="A",
                quantity=1
            )
        ]
    )
    response = client.post("/purchase", json=data.dict())
    assert response.status_code == 400 or response.status_code == 422  # バリデーションでエラーになる想定

def test_create_transaction_with_invalid_tax_cd(client):
    data = TransactionCreate(
        emp_cd="E004",
        store_cd="S004",
        pos_no="04",
        details=[
            TransactionDetailCreate(  # ← 修正ポイント
                prd_code="4901480325118",
                prd_name="異常税区分商品",
                prd_price=380,
                tax_cd="Z",  # 不正な税区分
                quantity=1
            )
        ]
    )
    response = client.post("/purchase", json=data.model_dump())  # Pydantic v2に合わせて model_dump を使用
    assert response.status_code == 400 or response.status_code == 422  # バリデーションエラー想定
