# schemas/transaction.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Transaction(BaseModel):
    maphieu: str
    ngaynx: datetime
    loaiphieu: str
    diengiai: Optional[str]
    makho: str

class TransactionCreate(BaseModel):
    maphieu: str
    ngaynx: datetime
    loaiphieu: str
    diengiai: Optional[str]
    makho: str

class TransactionResponse(BaseModel):
    data: List[Transaction]