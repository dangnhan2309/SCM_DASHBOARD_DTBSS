from db import execute_query

def get_all_vattu(site: str = "NAM"):
    """
    Lấy danh mục vật tư từ một site cụ thể (Mặc định là NAM).
    Sử dụng Alias với dấu nháy kép để khớp chính xác với Pydantic Model.
    """
    
    # Ép tên cột trả về thành MaVT, TenVT... để khớp với Model MaVT, TenVT...
    query = """
    SELECT 
        MaVT AS "MaVT", 
        TenVT AS "TenVT", 
        DonViTinh AS "DonViTinh", 
        LoaiVT AS "LoaiVT" 
    FROM VatTu
    """
    
    # Khai báo params trống để đúng format của execute_query
    params = {}

    return execute_query(site, query, params)


from db import execute_query

def get_gia_von_by_site(site: str):
    # Cập nhật query theo đúng các cột: MAVT, GIACHUAN, GIATHUCTE, NAMTAICHINH
    query = """
    SELECT 
        MAVT AS "MaVT", 
        GIACHUAN AS "GiaChuan", 
        GIATHUCTE AS "GiaThucTe", 
        NAMTAICHINH AS "NamTaiChinh"
    FROM GIAVON
    """
    params = {}
    return execute_query(site, query, params)