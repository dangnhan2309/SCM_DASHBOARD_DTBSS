# schemas/alert.py
from pydantic import BaseModel
from typing import List

class LowStockItem(BaseModel):
    mavt: str
    tenvt: str
    soluong: int
    nguong_toithieu: int

class AlertResponse(BaseModel):
    data: List[LowStockItem]