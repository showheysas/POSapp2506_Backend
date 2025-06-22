from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import product, purchase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://posapp2506-frontend-r2.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(product.router)
app.include_router(purchase.router)
