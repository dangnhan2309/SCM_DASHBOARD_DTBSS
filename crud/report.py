from db import execute_query

def join_tonkho_giavon():
    """
    Báo cáo tổng hợp kết hợp Phân tán Dọc (GiaVon tại NAM) 
    và Phân mảnh Ngang (TonKho tại các Site).
    Thực thi duy nhất tại Site NAM.
    """
    
    query = """
    SELECT 
        v.TenVT AS "TenVT", 
        tk.SoLuongTon AS "SoLuongTon", 
        gv.GiaThucTe AS "GiaThucTe", 
        (tk.SoLuongTon * gv.GiaThucTe) AS "TongGiaTri",
        'Site NAM' AS "NguonDuLieu"
    FROM TonKho tk
    JOIN VatTu v ON tk.MaVT = v.MaVT
    JOIN GiaVon gv ON tk.MaVT = gv.MaVT
    
    UNION ALL
    
    SELECT 
        v.TenVT AS "TenVT", 
        tk.SoLuongTon AS "SoLuongTon", 
        gv.GiaThucTe AS "GiaThucTe", 
        (tk.SoLuongTon * gv.GiaThucTe) AS "TongGiaTri",
        'Site BAC' AS "NguonDuLieu"
    FROM TonKho@to_bac tk
    JOIN VatTu v ON tk.MaVT = v.MaVT
    JOIN GiaVon gv ON tk.MaVT = gv.MaVT
    
    UNION ALL
    
    SELECT 
        v.TenVT AS "TenVT", 
        tk.SoLuongTon AS "SoLuongTon", 
        gv.GiaThucTe AS "GiaThucTe", 
        (tk.SoLuongTon * gv.GiaThucTe) AS "TongGiaTri",
        'Site TRUNG' AS "NguonDuLieu"
    FROM TonKho@to_trung tk
    JOIN VatTu v ON tk.MaVT = v.MaVT
    JOIN GiaVon gv ON tk.MaVT = gv.MaVT
    """

    # Format tách biệt params
    params = {}

    return execute_query("NAM", query, params)