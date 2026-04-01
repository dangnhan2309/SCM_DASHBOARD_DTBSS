from fastapi import APIRouter, Query
from typing import List
from models.vattu import VatTu # Import model mới
from crud import vattu as crud_vattu
from models.giavon import GiaVon
from fastapi import HTTPException


router = APIRouter(prefix="/vattu", tags=["Vật Tư"])

@router.get("/", response_model=List[VatTu])
async def read_vattu(site: str = Query("NAM")):
    return crud_vattu.get_all_vattu(site)
@router.get("/giavon", response_model=List[GiaVon])
async def read_gia_von(site: str = Query(...)):
    try:
        # Ép kiểu site lên chữ hoa để tránh lỗi config
        data = crud_vattu.get_gia_von_by_site(site.upper())
        
        if not data:
            return []
        return data
    except Exception as e:
        # Trả về lỗi 404 để chứng minh bảng không tồn tại ở Site này
        raise HTTPException(
            status_code=404, 
            detail=f"Table 'GIAVON' is not fragmented to Site {site}. (Vertical Fragmentation Proof)"
        )