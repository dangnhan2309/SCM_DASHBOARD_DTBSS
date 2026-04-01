from pydantic import BaseModel, Field
from typing import Optional

class Phieu(BaseModel):
    MaPhieu: str = Field(..., min_length=2, max_length=10, description="Mã phiếu, ví dụ: PN001")
    NgayNX: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Định dạng YYYY-MM-DD")
    LoaiPhieu: str = Field(..., pattern="^(N|X)$", description="N: Nhập, X: Xuất")
    DienGiai: Optional[str] = Field(None, max_length=200)
    MaKho: str = Field(..., max_length=10)
    site: str = Field(..., pattern="^(BAC|TRUNG|NAM)$", description="Site đích để thực thi")

    class Config:
        json_schema_extra = {
            "example": {
                "MaPhieu": "PN001",
                "NgayNX": "2026-04-01",
                "LoaiPhieu": "N",
                "DienGiai": "Nhập hàng tồn kho đầu kỳ",
                "MaKho": "KHO01",
                "site": "NAM"
            }
        }