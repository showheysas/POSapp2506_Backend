def test_create_transaction_success(client, test_db):
    payload = {
        "emp_cd": "9999999999",
        "store_cd": "00030",
        "pos_no": "090",
        "details": [
            {
                "prd_code": "4901480151908",
                "prd_name": "テープのり〈ドットライナー〉（本体）",
                "prd_price": 460,
                "tax_cd": "01",
                "quantity": 2
            },
            {
                "prd_code": "4901480325118",
                "prd_name": "鉛筆シャープTypeS",
                "prd_price": 380,
                "tax_cd": "01",
                "quantity": 1
            }
        ]
    }
    response = client.post("/purchase", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_amount"] == 1300
    assert data["total_amount_ex_tax"] == 1181  # 税抜換算（例：460+700→/1.1）

def test_create_transaction_empty_details(client):
    payload = {
        "emp_cd": "EMP001",
        "store_cd": "S001",
        "pos_no": "001",
        "details": []
    }
    response = client.post("/purchase", json=payload)
    assert response.status_code == 422
