from pydantic import BaseModel

class GiaVon(BaseModel):
    MaVT: str
    GiaChuan: float
    GiaThucTe: float
    NamTaiChinh: int