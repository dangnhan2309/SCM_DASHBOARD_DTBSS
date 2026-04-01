from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Cấu hình chuỗi kết nối (Thay đổi User/Pass/Host/Service cho đúng thực tế)
DB_CONFIGS = {
    # Site BAC chạy cổng 1524
    "BAC": "oracle+oracledb://bac:123@localhost:1524/?service_name=pdb_bac",
    
    # Site TRUNG chạy cổng 1522
    "TRUNG": "oracle+oracledb://trung:123@localhost:1522/?service_name=pdb_trung",
    
    # Site NAM chạy cổng 1523
    "NAM": "oracle+oracledb://nam:123@localhost:1523/?service_name=pdb_nam"
}
# Dictionary lưu trữ các engine đã khởi tạo
engines = {}

def get_engine(site: str) -> Engine:
    site = site.upper()
    if site not in DB_CONFIGS:
        raise ValueError(f"Site {site} không hợp lệ!")
    
    if site not in engines:
        # pool_size giúp duy trì các kết nối sẵn có để tăng tốc độ
        engines[site] = create_engine(DB_CONFIGS[site], pool_pre_ping=True)
    
    return engines[site]

def execute_query(site: str, query: str, params: dict = None):
    engine = get_engine(site)
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        # Trả về danh sách dictionary để FastAPI dễ convert sang JSON
        if result.returns_rows:
            return [dict(row._mapping) for row in result]
        connection.commit()
        return {"status": "success"}