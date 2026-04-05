# from sqlalchemy import create_engine, text
# from sqlalchemy.engine import Engine

# # Cấu hình chuỗi kết nối (Thay đổi User/Pass/Host/Service cho đúng thực tế)
# DB_CONFIGS = {
#     # Site BAC chạy cổng 1524
#     "BAC": "oracle+oracledb://bac:123@localhost:1524/?service_name=pdb_bac",
    
#     # Site TRUNG chạy cổng 1522
#     "TRUNG": "oracle+oracledb://trung:123@localhost:1522/?service_name=pdb_trung",
    
#     # Site NAM chạy cổng 1523
#     "NAM": "oracle+oracledb://nam:123@localhost:1523/?service_name=pdb_nam"
# }
# # Dictionary lưu trữ các engine đã khởi tạo
# engines = {}

# def get_engine(site: str) -> Engine:
#     site = site.upper()
#     if site not in DB_CONFIGS:
#         raise ValueError(f"Site {site} không hợp lệ!")
    
#     if site not in engines:
#         # pool_size giúp duy trì các kết nối sẵn có để tăng tốc độ
#         engines[site] = create_engine(DB_CONFIGS[site], pool_pre_ping=True)
    
#     return engines[site]

# def execute_query(site: str, query: str, params: dict = None):
#     engine = get_engine(site)
#     with engine.connect() as connection:
#         result = connection.execute(text(query), params or {})
#         # Trả về danh sách dictionary để FastAPI dễ convert sang JSON
#         if result.returns_rows:
#             return [dict(row._mapping) for row in result]
#         connection.commit()
#         return {"status": "success"}



from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import oracledb

# Cấu hình chuỗi kết nối (Cập nhật đúng thông tin thực tế của bạn)
DB_CONFIGS = {
    "BAC": "oracle+oracledb://bac:123@localhost:1524/?service_name=pdb_bac",
    "TRUNG": "oracle+oracledb://trung:123@localhost:1522/?service_name=pdb_trung",
    "NAM": "oracle+oracledb://nam:123@localhost:1523/?service_name=pdb_nam"
}

engines = {}

def get_engine(site: str) -> Engine:
    site = site.upper()
    if site not in DB_CONFIGS:
        raise ValueError(f"Site {site} không hợp lệ!")
    
    if site not in engines:
        # pool_pre_ping giúp tự động kết nối lại nếu DB bị ngắt quãng
        engines[site] = create_engine(
            DB_CONFIGS[site], 
            pool_size=5, 
            max_overflow=10, 
            pool_pre_ping=True
        )
    return engines[site]

def get_db_connection(site: str):
    """
    Lấy kết nối raw từ driver oracledb để xử lý các tác vụ phức tạp 
    như REF CURSOR hoặc gọi Procedure trực tiếp.
    """
    engine = get_engine(site)
    # Trả về kết nối gốc của driver (DBAPI connection)
    return engine.raw_connection()

def execute_query(site: str, query: str, params: dict = None):
    """
    Thực thi các câu lệnh SQL thông thường (SELECT, INSERT, UPDATE, DELETE).
    """
    engine = get_engine(site)
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            
            # Nếu là câu lệnh SELECT
            if result.returns_rows:
                return [dict(row._mapping) for row in result]
            
            # Nếu là câu lệnh thay đổi dữ liệu
            connection.commit()
            return {"status": "success"}
    except Exception as e:
        print(f"Lỗi thực thi query tại {site}: {e}")
        raise e