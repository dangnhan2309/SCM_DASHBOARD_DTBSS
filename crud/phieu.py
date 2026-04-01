from db import execute_query

from db import execute_query

def create_phieu(site: str, data: dict):
    query = """
    INSERT INTO PhieuNhapXuat 
    (MaPhieu, NgayNX, LoaiPhieu, DienGiai, MaKho)
    VALUES 
    (:MaPhieu, TO_DATE(:NgayNX, 'YYYY-MM-DD'), :LoaiPhieu, :DienGiai, :MaKho)
    """

    params = {
        "MaPhieu": data.get("MaPhieu"),
        "NgayNX": data.get("NgayNX"),
        "LoaiPhieu": data.get("LoaiPhieu"),
        "DienGiai": data.get("DienGiai"),
        "MaKho": data.get("MaKho")
    }

    return execute_query(site, query, params)
def create_chitiet(site: str, data: dict):
    query = """
    INSERT INTO ChiTietPhieu 
    (MaPhieu, MaVT, SoLuong)
    VALUES 
    (:MaPhieu, :MaVT, :SoLuong)
    """

    params = {
        "MaPhieu": data.get("MaPhieu"),
        "MaVT": data.get("MaVT"),
        "SoLuong": data.get("SoLuong")
    }

    return execute_query(site, query, params)

def create_full_phieu(site: str, phieu: dict, chitiet_list: list):
    # 1. insert phiếu
    create_phieu(site, phieu)

    # 2. insert chi tiết
    for item in chitiet_list:
        item["MaPhieu"] = phieu["MaPhieu"]
        create_chitiet(site, item)

    return {"status": "success", "message": "Tạo phiếu hoàn chỉnh"}