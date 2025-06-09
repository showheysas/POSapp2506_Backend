from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import product, purchase

app = FastAPI()

# CORS設定（Next.jsと接続するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(product.router)
app.include_router(purchase.router)
