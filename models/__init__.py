from sqlalchemy.orm import declarative_base
Base = declarative_base()

from .product_master import ProductMaster
from .transaction import Transaction, TransactionDetail 

# メタデータに登録（検出用）
ProductMaster
Transaction
TransactionDetail