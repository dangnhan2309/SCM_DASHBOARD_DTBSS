# routers/overview.py
from fastapi import APIRouter
from db import execute_query
from typing import List, Dict, Any

router = APIRouter()

def get_total(data: List[Dict[str, Any]]) -> int:
    return int(data[0]["TOTAL".lower()]) if data else 0


@router.get("/overview")
def get_overview():
    bac = execute_query("BAC", "SELECT NVL(SUM(SoLuongTon),0) total FROM TonKho")
    trung = execute_query("TRUNG", "SELECT NVL(SUM(SoLuongTon),0) total FROM TonKho")
    nam = execute_query("NAM", "SELECT NVL(SUM(SoLuongTon),0) total FROM TonKho")

    total_inventory = get_total(bac) + get_total(trung) + get_total(nam)

    lsx = execute_query("NAM", "SELECT COUNT(*) total FROM LenhSanXuat")
    trans = execute_query("NAM", "SELECT COUNT(*) total FROM PhieuNhapXuat")

    return {
        "total_inventory": total_inventory,
        "total_lsx": get_total(lsx),
        "total_transactions": get_total(trans)
    }


@router.get("/inventory/summary")
def inventory_summary():
    result = []
    for site in ["BAC", "TRUNG", "NAM"]:
        data = execute_query(site, "SELECT NVL(SUM(SoLuongTon),0) total FROM TonKho")
        result.append({
            "site": site,
            "total_quantity": get_total(data)
        })
    return result