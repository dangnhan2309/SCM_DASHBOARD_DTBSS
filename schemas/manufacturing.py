# schemas/manufacturing.py
from pydantic import BaseModel
from typing import Optional

class LSX(BaseModel):
    malsx: str
    soluong: int
    makho: str
    trangthai: Optional[str]

class LSXCreate(BaseModel):
    malsx: str
    soluong: int
    makho: str

class LSXResponse(BaseModel):
    data: list[LSX]