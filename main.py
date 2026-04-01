from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import execute_query
from crud import vattu, tonkho, phieu, report
from routers import vattu, tonkho, phieu, report
app = FastAPI(title="HUTECH Distributed DB System")

# Enable CORS để gọi API từ Web/Mobile không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Đăng ký các router
app.include_router(vattu.router)
app.include_router(tonkho.router)
app.include_router(phieu.router)
app.include_router(report.router)
@app.get("/")
async def root():
    return {"message": "Welcome to Distributed Database API Phase 1"}


@app.get("/vattu")
def read_vattu():
    return vattu.get_all_vattu()

@app.get("/tonkho/global")
def read_global_inventory():
    return tonkho.get_tonkho_global()

@app.get("/report/costing")
def get_cost_report():
    return report.join_tonkho_giavon()








@app.get("/test-connection/{site}")
async def test_connection(site: str):
    """Route test thử xem có kết nối được tới DB của Site đó không"""
    try:
        # Thử truy vấn bảng dual đặc trưng của Oracle
        data = execute_query(site, "SELECT 'Connection OK' as status FROM dual")
        return {"site": site.upper(), "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chạy lệnh: uvicorn main:app --reload