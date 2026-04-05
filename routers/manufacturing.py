# routers/manufacturing.py
from typing import Optional

from fastapi import APIRouter
from db import execute_query

router = APIRouter()

def get_site_by_makho(makho):
    if makho.startswith("B"):
        return "BAC"
    elif makho.startswith("T"):
        return "TRUNG"
    return "NAM"


@router.get("/lsx")
def get_lsx(status: Optional[str] = None):
    query = "SELECT * FROM LenhSanXuat"
    params = {}

    if status:
        query += " WHERE TrangThai = :status"
        params["status"] = status

    return execute_query("NAM", query, params)


@router.post("/lsx")
def create_lsx(data: dict):
    site = get_site_by_makho(data["makho"])

    query = """
    INSERT INTO LenhSanXuat (MaLSX, SoLuong, MaKho)
    VALUES (:malsx, :soluong, :makho)
    """

    return execute_query(site, query, data)