# routers/transactions.py
from fastapi import APIRouter
from db import execute_query

router = APIRouter()

def get_site_by_makho(makho):
    if makho.startswith("B"):
        return "BAC"
    elif makho.startswith("T"):
        return "TRUNG"
    return "NAM"


@router.get("/transactions")
def get_transactions():
    result = []
    for site in ["BAC", "TRUNG", "NAM"]:
        data = execute_query(site, "SELECT * FROM PhieuNhapXuat")
        result.extend(data)
    return result


@router.get("/transactions/nhap")
def get_transactions_by_month(month: int):
    query = """
    SELECT * FROM PhieuNhapXuat
    WHERE EXTRACT(MONTH FROM NgayNX) = :month
    """
    result = []
    for site in ["BAC", "TRUNG", "NAM"]:
        data = execute_query(site, query, {"month": month})
        result.extend(data)
    return result


@router.post("/transactions")
def create_transaction(data: dict):
    site = get_site_by_makho(data["makho"])

    query = """
    INSERT INTO PhieuNhapXuat (MaPhieu, NgayNX, LoaiPhieu, DienGiai, MaKho)
    VALUES (:maphieu, :ngaynx, :loaiphieu, :diengiai, :makho)
    """

    return execute_query(site, query, data)