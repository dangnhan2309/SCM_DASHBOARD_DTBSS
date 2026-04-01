from fastapi import APIRouter
from crud.report import join_tonkho_giavon

router = APIRouter(prefix="/report", tags=["Báo Cáo Phân Tán"])

@router.get("/tonkho-giavon")
async def get_report():
    """Báo cáo kết hợp Phân tán Dọc (GiaVon) và Phân tán Ngang (TonKho)"""
    return join_tonkho_giavon()