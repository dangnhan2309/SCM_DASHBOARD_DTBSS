# schemas/overview.py
from pydantic import BaseModel

class OverviewResponse(BaseModel):
    total_inventory: int
    total_value: float
    total_lsx: int
    total_transactions: int