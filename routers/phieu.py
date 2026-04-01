from fastapi import APIRouter, HTTPException
from models.phieu import Phieu
from models.chitiet import ChiTietPhieu
from crud import phieu as crud_phieu

router = APIRouter(prefix="/phieu", tags=["Nghiệp Vụ Phiếu"])

@router.post("/")
async def add_phieu(data: Phieu):
    # data lúc này đã là một object có type-hint cực xịn
    try:
        return crud_phieu.create_phieu(data.site, data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chi-tiet")
async def add_chi_tiet(data: ChiTietPhieu):
    try:
        return crud_phieu.create_chitiet(data.site, data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))