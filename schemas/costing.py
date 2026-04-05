# schemas/costing.py
from pydantic import BaseModel
from typing import List

class GiaVon(BaseModel):
    mavt: str
    giavon: float

class BOMItem(BaseModel):
    mavt: str
    nguyenlieu: str
    soluong: float

class BOMUpdate(BaseModel):
    mavt: str
    soluong: float

class GiaVonResponse(BaseModel):
    data: List[GiaVon]

class BOMResponse(BaseModel):
    data: List[BOMItem]