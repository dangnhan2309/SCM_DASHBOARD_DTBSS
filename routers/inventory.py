from fastapi import APIRouter, HTTPException
from db import execute_query,get_engine, get_db_connection  # Giả sử bạn có hàm lấy connection trực tiếp
import oracledb

router = APIRouter()

@router.get("/inventory/{mavt}")
def get_inventory(mavt: str):
    # Dùng raw connection để xử lý REF CURSOR
    conn = get_db_connection("BAC")
    try:
        cursor = conn.cursor()
        ref_cursor = conn.cursor()
        cursor.callproc("usp_TraCuuTonKho", [mavt, ref_cursor])
        
        columns = [col[0] for col in ref_cursor.description]
        data = [dict(zip(columns, row)) for row in ref_cursor.fetchall()]
        return data
    finally:
        conn.close() # Trả kết nối về pool

@router.get("/inventory/by-warehouse")
def inventory_by_warehouse():
    """
    Gộp dữ liệu tồn kho từ cả 3 Site (Distributed Query)
    """
    result = []
    sites = ["BAC", "TRUNG", "NAM"]
    
    for site in sites:
        try:
            # Truy vấn bảng TonKho tại từng site
            data = execute_query(site, "SELECT * FROM TonKho")
            # Thêm thông tin Site để UI dễ phân biệt
            for item in data:
                item["SITE_SOURCE"] = site
            result.extend(data)
        except Exception as e:
            # Nếu 1 site sập, vẫn trả về dữ liệu các site còn lại và log lỗi
            print(f"Warning: Site {site} is unreachable. Error: {e}")
            
    return result

@router.get("/inventory/value/{makho}")
def inventory_value(makho: str):
    """
    Tính giá trị tồn kho tại Site BAC.
    Kết nối DBLINK tới Site NAM để lấy giá vốn và trả về kết quả qua REF CURSOR.
    """
    # 1. Lấy kết nối raw từ Site BAC
    conn = get_db_connection("BAC")
    
    try:
        cursor = conn.cursor()
        # 2. Tạo một cursor mới để hứng tham số OUT (p_Cursor)
        out_cursor = conn.cursor()
        
        # 3. Gọi Procedure: usp_TinhGiaTriTonKho(p_MaKho, p_Cursor)
        # Chú ý: Thứ tự tham số trong list phải khớp với Procedure trong SQL
        cursor.callproc("usp_TinhGiaTriTonKho", [makho, out_cursor])
        
        # 4. Fetch dữ liệu từ out_cursor và chuyển thành danh sách Dictionary
        columns = [col[0] for col in out_cursor.description]
        result = [dict(zip(columns, row)) for row in out_cursor.fetchall()]
        
        # dọn dẹp cursor phụ
        out_cursor.close()
        cursor.close()
        
        if not result:
            return {"message": f"Không có dữ liệu tồn kho cho kho {makho}", "data": []}
            
        return {
            "status": "success",
            "site": "BAC",
            "makho": makho,
            "data": result
        }

    except Exception as e:
        # Log lỗi chi tiết để dễ debug
        print(f"Lỗi khi gọi usp_TinhGiaTriTonKho: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    
    finally:
        # Luôn luôn đóng connection để trả về pool, tránh treo database
        conn.close()