# schemas/global_schema.py
from pydantic import BaseModel

class GlobalInventoryResponse(BaseModel):
    mavt: str
    total_quantity: int

class GlobalTransactionCount(BaseModel):
    year: int
    total_transactions: int