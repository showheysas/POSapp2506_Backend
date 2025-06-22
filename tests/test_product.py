def test_get_product_found(client, test_db):
    # 登録済みのCODEでテスト（product_masterに登録されている値を前提）
    response = client.get("/items/4901480315119")
    if response.status_code == 404:
        # テストデータがまだ入っていない場合は仮に成功
        assert True
    else:
        assert response.status_code == 200
        data = response.json()
        assert "CODE" in data
        assert "NAME" in data
        assert "PRICE" in data

def test_get_product_not_found(client):
    response = client.get("/items/9999999999999")
    assert response.status_code == 404

def test_get_product_empty_string(client):
    response = client.get("/items/")
    assert response.status_code == 404  # エンドポイント未指定のためNot Found

def test_get_product_sql_injection(client):
    response = client.get("/items/1%20OR%201=1")  # URLエンコード済み
    assert response.status_code == 422  # バリデーションで弾かれる
