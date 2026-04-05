from fastapi import APIRouter, HTTPException
from db import execute_query

router = APIRouter()

@router.get("/alerts/low-stock")
def low_stock():
    """
    Truy vấn View cảnh báo hết hàng từ cả 3 Site.
    """
    all_alerts = []
    sites = ["BAC", "TRUNG", "NAM"]
    
    for site in sites:
        try:
            # Truy vấn View tại mỗi Site
            # Lưu ý: Đảm bảo vw_CanhBaoHetHang đã được CREATE VIEW tại mỗi DB
            data = execute_query(site, "SELECT * FROM vw_CanhBaoHetHang")
            
            if data and isinstance(data, list):
                # Thêm nhãn nguồn (Source) để Dashboard Streamlit 
                # có thể hiển thị: "Sản phẩm A sắp hết tại kho MIỀN BẮC"
                for item in data:
                    item["SITE_LOCATION"] = site
                
                all_alerts.extend(data)
                
        except Exception as e:
            # Quan trọng: Nếu Site Trung sập, API vẫn phải trả về dữ liệu 
            # của Site Bắc và Nam thay vì văng lỗi 500 toàn hệ thống.
            print(f"⚠️ Cảnh báo: Không thể kết nối tới Site {site}. Chi tiết: {e}")
            continue 

    # Nếu không có site nào trả về dữ liệu
    if not all_alerts:
        return {"message": "Hiện tại không có cảnh báo hết hàng hoặc các Site mất kết nối.", "data": []}

    return all_alerts