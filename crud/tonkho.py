from db import execute_query

# Lấy tồn kho tại 1 site cụ thể
def get_tonkho_by_site(site: str):
    # Sử dụng AS với dấu nháy kép để ép tên cột khớp với Pydantic (MaKho, MaVT...)
    query = """
    SELECT 
        MaKho AS "MaKho", 
        MaVT AS "MaVT", 
        SoLuongTon AS "SoLuongTon", 
        MinStock AS "MinStock", 
        MaxStock AS "MaxStock" 
    FROM TonKho
    """
    params = {} # Không có tham số truyền vào nhưng giữ đúng format
    return execute_query(site, query, params)

# Lấy tồn kho toàn cục bằng DB LINK (Chạy tại Site NAM)
def get_tonkho_global():
    # Lưu ý: Khi dùng t.*, Oracle sẽ trả về tên cột CHỮ HOA (MAKHO). 
    # Ta nên liệt kê chi tiết để Pydantic không bị lỗi "missing field".
    query = """
    SELECT 'MIEN NAM' AS "KhuVuc", MaKho AS "MaKho", MaVT AS "MaVT", 
           SoLuongTon AS "SoLuongTon", MinStock AS "MinStock", MaxStock AS "MaxStock" 
    FROM TonKho
    
    UNION ALL
    
    SELECT 'MIEN TRUNG' AS "KhuVuc", MaKho AS "MaKho", MaVT AS "MaVT", 
           SoLuongTon AS "SoLuongTon", MinStock AS "MinStock", MaxStock AS "MaxStock" 
    FROM TonKho@to_trung
    
    UNION ALL
    
    SELECT 'MIEN BAC' AS "KhuVuc", MaKho AS "MaKho", MaVT AS "MaVT", 
           SoLuongTon AS "SoLuongTon", MinStock AS "MinStock", MaxStock AS "MaxStock" 
    FROM TonKho@to_bac
    """
    params = {}
    return execute_query("NAM", query, params)