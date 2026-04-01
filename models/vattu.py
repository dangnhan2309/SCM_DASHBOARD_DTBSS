# models/vattu.py
from pydantic import BaseModel

class VatTu(BaseModel):
    MaVT: str
    TenVT: str
    DonViTinh: str
    LoaiVT: str

# models/tonkho.py
from pydantic import BaseModel
from typing import Optional

class TonKho(BaseModel):
    KhuVuc: Optional[str] = None # Dùng cho Global View
    MaKho: str
    MaVT: str
    SoLuongTon: float
    MinStock: float
    MaxStock: float