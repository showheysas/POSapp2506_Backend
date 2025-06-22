from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

# Supabaseの接続情報（Renderの環境変数から読み込む）
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL用のエンジン作成（SSL接続が必要）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"}  # Supabaseでは必須
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
