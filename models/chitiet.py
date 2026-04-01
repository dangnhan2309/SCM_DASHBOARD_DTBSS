from pydantic import BaseModel, Field

class ChiTietPhieu(BaseModel):
    MaPhieu: str = Field(..., max_length=10)
    MaVT: str = Field(..., max_length=10)
    SoLuong: float = Field(..., gt=0, description="Số lượng phải lớn hơn 0")
    site: str = Field(..., pattern="^(BAC|TRUNG|NAM)$")

    class Config:
        json_schema_extra = {
            "example": {
                "MaPhieu": "PN001",
                "MaVT": "VT01",
                "SoLuong": 150.5,
                "site": "NAM"
            }
        }