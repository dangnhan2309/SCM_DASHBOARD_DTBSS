# schemas/inventory.py
from pydantic import BaseModel
from typing import List

class InventoryItem(BaseModel):
    mavt: str
    tenvt: str
    makho: str
    soluong: int

class InventoryDetailResponse(BaseModel):
    mavt: str
    total_quantity: int
    sites: List[InventoryItem]

class InventorySummary(BaseModel):
    site: str
    total_quantity: int

class InventoryValueResponse(BaseModel):
    makho: str
    total_value: float