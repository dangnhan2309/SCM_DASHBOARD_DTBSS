# routers/global_query.py
from fastapi import APIRouter
from db import execute_query

router = APIRouter()


@router.get("/global/inventory/{mavt}")
def global_inventory(mavt: str):
    query = """
    SELECT SUM(SoLuongTon) total FROM (
        SELECT SoLuongTon FROM TonKho@TO_BAC WHERE MaVT = :mavt
        UNION ALL
        SELECT SoLuongTon FROM TonKho@TO_TRUNG WHERE MaVT = :mavt
        UNION ALL
        SELECT SoLuongTon FROM TonKho WHERE MaVT = :mavt
    )
    """
    return execute_query("NAM", query, {"mavt": mavt})


@router.get("/global/count-transactions")
def count_transactions(year: int):
    query = """
    SELECT COUNT(*) total FROM (
        SELECT MaPhieu FROM PhieuNhapXuat@TO_BAC WHERE EXTRACT(YEAR FROM NgayNX)=:year
        UNION ALL
        SELECT MaPhieu FROM PhieuNhapXuat@TO_TRUNG WHERE EXTRACT(YEAR FROM NgayNX)=:year
        UNION ALL
        SELECT MaPhieu FROM PhieuNhapXuat WHERE EXTRACT(YEAR FROM NgayNX)=:year
    )   
    """
    return execute_query("NAM", query, {"year": year})