# routers/costing.py
from fastapi import APIRouter
from db import execute_query

router = APIRouter()

@router.get("/costing/giavon")
def get_giavon():
    return execute_query("NAM", "SELECT * FROM GiaVon")


# @router.get("/costing/bom")
# def get_bom():
#     return execute_query("NAM", "SELECT * FROM BOM")


# @router.put("/costing/bom")
# def update_bom(data: dict):
#     query = """
#     UPDATE BOM
#     SET SoLuong = :soluong
#     WHERE MaVT = :mavt
#     """
#     return execute_query("NAM", query, data)