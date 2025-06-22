import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  # 重要

# パス設定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Base
from db import get_db
from main import app
from fastapi.testclient import TestClient
from models.product_master import ProductMaster

# SQLite インメモリDB（全テストで共有）
TEST_DB_URL = "sqlite://"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # ← これが肝
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# スキーマ作成（engineから）
Base.metadata.create_all(bind=engine)

# DBセッション fixture
@pytest.fixture(scope="function")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# テストクライアント fixture
@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
    with TestClient(app) as c:
        yield c

# 商品マスターにテストデータを投入（全テスト共通）
@pytest.fixture(scope="function", autouse=True)
def seed_product_master(test_db):
    test_db.query(ProductMaster).delete()
    test_db.commit()
    test_db.add_all([
        ProductMaster(CODE=4901480151908, NAME="テープのり〈ドットライナー〉（本体）", PRICE=460),
        ProductMaster(CODE=4901480325118, NAME="鉛筆シャープTypeS", PRICE=380),
    ])
    test_db.commit()
