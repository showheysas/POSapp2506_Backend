from pydantic import BaseModel, Field

# 商品コードで検索するときのパラメータ（必要なら使用）
class ProductCodeInput(BaseModel):
    code: int

# 商品情報を返すときのレスポンススキーマ
class ProductOut(BaseModel):
    code: int = Field(alias='CODE')
    name: str = Field(alias='NAME')
    price: int = Field(alias='PRICE')

    class Config:
        from_attributes = True
        populate_by_name = True  # エイリアス経由で値を受け取れる
