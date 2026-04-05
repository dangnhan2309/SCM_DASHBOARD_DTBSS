

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CẤU HÌNH ---
st.set_page_config(page_title="HUTECH Distributed DB Demo", layout="wide")
API_BASE_URL = "http://127.0.0.1:8000"

# Từ điển ánh xạ để hiển thị URL vật lý (Chứng minh tính minh bạch vị trí)
SITE_MAP = {
    "BAC": {"port": "1524", "pdb": "pdb_bac", "name": "Miền Bắc"},
    "TRUNG": {"port": "1522", "pdb": "pdb_trung", "name": "Miền Trung"},
    "NAM": {"port": "1523", "pdb": "pdb_nam", "name": "Miền Nam (Trụ sở)"},
    "GLOBAL": {"port": "N/A", "pdb": "CDB$ROOT / DBLINK", "name": "Toàn hệ thống"}
}

st.title("🚀 Hệ Quản Trị CSDL Phân Tán - ERP Logistics")

# --- 5. GIAO DIỆN GỢI Ý (SIDEBAR) ---
st.sidebar.header("🕹️ Điều khiển Hệ thống")
site_selected = st.sidebar.selectbox(
    "Giả lập quyền truy cập tại Site:",
    ["GLOBAL", "BAC", "TRUNG", "NAM"],
    help="Chọn site để chứng minh các mảnh dữ liệu tương ứng."
)

# Hiển thị URL API để chứng minh kết nối vật lý (Yêu cầu 1)
if site_selected != "GLOBAL":
    info = SITE_MAP[site_selected]
    st.sidebar.success(f"🔗 Đang kết nối tới: \nhttp://localhost:{info['port']}/{info['pdb']}")
else:
    st.sidebar.info("🌐 Chế độ Global: Sử dụng Gateway DBLINK từ Site NAM")

# --- PHÂN CHIA TAB ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 1. Logistics (Ngang)", 
    "💰 2. Trụ sở (Dọc)", 
    "📋 3. Danh mục (Nhân bản)", 
    "📈 4. Báo cáo hợp nhất"
])

# --- 1. CHỨNG MINH PHÂN MẢNH NGANG ---
with tab1:
    st.header("🏢 Quản lý Kho Miền")
    if st.button(f"🔍 Truy vấn Kho tại {site_selected}"):
        url = f"{API_BASE_URL}/tonkho/{site_selected.lower()}" if site_selected != "GLOBAL" else f"{API_BASE_URL}/tonkho/global"
        res = requests.get(url)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            
            # Biểu đồ vùng miền (Yêu cầu 1)
            st.write(f"### Dữ liệu tồn kho thực tế tại trạm")
            st.dataframe(df, use_container_width=True)
            
            fig = px.bar(df, x="MaVT", y="SoLuongTon", color="MaKho", 
                         title=f"Biểu đồ tồn kho của {site_selected}")
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"💡 Giải thích: Tại trạm {site_selected}, chúng ta chỉ thấy dữ liệu kho thuộc quyền quản lý của miền đó.")

# --- 2. CHỨNG MINH PHÂN TÁN DỌC ---
with tab2:
    st.header("🛡️ Bảo mật & Phân tán Dọc")
    st.write("Yêu cầu: Thông tin Giá vốn và Định mức chỉ lưu tại Trụ sở (NAM).")
        
    if st.button("⚖️ Kiểm tra bảng Giá vốn"):
        res = requests.get(f"{API_BASE_URL}/vattu/giavon?site={site_selected}")
        
        if res.status_code == 200:
            data = res.json()
            if data:
                st.success(f"✅ Truy cập thành công bảng GIAVON tại {site_selected}")
                df = pd.DataFrame(data)
                st.table(df) # Dùng st.table để hiện danh sách giá chuẩn/thực tế
            else:
                st.info("Bảng tồn tại nhưng không có dữ liệu cho năm tài chính này.")
        else:
            # Hiển thị lỗi đỏ để chứng minh Phân tán dọc
            err = res.json().get("detail")
            st.error(f"🔴 {err}")
# --- 3. CHỨNG MINH NHÂN BẢN ---
with tab3:
    st.header("📑 Danh mục Vật tư Nhân bản")
    st.write("Yêu cầu: Danh mục vật tư phải giống hệt nhau ở mọi site.")
    
    if st.button("🔄 So sánh dữ liệu Nhân bản (3 Site)"):
        col_b1, col_b2, col_b3 = st.columns(3)
        for s, col in zip(["BAC", "TRUNG", "NAM"], [col_b1, col_b2, col_b3]):
            with col:
                st.write(f"**Site {s}**")
                res = requests.get(f"{API_BASE_URL}/vattu?site={s}")
                if res.status_code == 200:
                    st.dataframe(pd.DataFrame(res.json())[["MaVT", "TenVT"]], hide_index=False)
        
        st.success("📢 Thông điệp: Mã vật tư ở cả 3 bảng đều giống hệt nhau. Chi nhánh có thể lập phiếu tức thì mà không cần hỏi server trung tâm.")

# --- 4. BÁO CÁO HỢP NHẤT (THE BIG DEMO) ---
with tab4:
    st.header("📊 Global Consolidated Report")
    if st.button("🔥 Refresh Global (DB Link Execution)"):
        res = requests.get(f"{API_BASE_URL}/report/tonkho-giavon")
        if res.status_code == 200:
            df_report = pd.DataFrame(res.json())
            
            # Metric Cards (Yêu cầu 4)
            m1, m2 = st.columns(2)
            total_stock = df_report["SoLuongTon"].sum()
            total_val = df_report["TongGiaTri"].sum()
            
            m1.metric("📦 Tổng lượng tồn (Toàn quốc)", f"{total_stock:,.0f} đơn vị")
            m2.metric("💸 Tổng giá trị tài sản", f"{total_val:,.0f} VNĐ")
            
            st.write("### Bảng dữ liệu hợp nhất từ DBLINK")
            st.table(df_report)
            
            st.info("💡 Đây là sự kết hợp: Lấy số lượng từ 3 Site (Ngang) JOIN với giá từ Site NAM (Dọc) qua DB Link.")

# --- Sidebar Footer ---
st.sidebar.markdown("---")
if st.sidebar.button("🛠️ Kiểm tra kết nối DB Link"):
    # Giả lập check status
    st.sidebar.code("BAC_DB -> OK\nTRUNG_DB -> OK\nNAM_DB -> OK")









# import streamlit as st
# import pandas as pd
# import numpy as np

# # =========================
# # CONFIG
# # =========================
# st.set_page_config(page_title="SCM Distributed Dashboard", layout="wide")

# # =========================
# # CSS
# # =========================
# st.markdown("""
# <style>
# .main {background-color: #f5f5f5;}
# div[data-testid="stMetric"] {
#     background-color: white;
#     padding: 15px;
#     border-radius: 12px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.05);
# }
# </style>
# """, unsafe_allow_html=True)

# # =========================
# # MOCK DATA (THAY BẰNG ORACLE)
# # =========================
# def fake_inventory():
#     return pd.DataFrame({
#         "MaKho": ["K01", "K02", "K03"],
#         "TenKho": ["Bac", "Trung", "Nam"],
#         "SoLuongTon": [100, 50, 200]
#     })

# def fake_transactions():
#     return pd.DataFrame({
#         "MaPhieu": ["P01", "P02"],
#         "Ngay": ["2025-04-01", "2025-04-02"],
#         "Loai": ["NhapMua", "Xuat"],
#         "DienGiai": ["Nhap CPU", "Xuat RAM"]
#     })

# def fake_lsx():
#     return pd.DataFrame({
#         "MaLSX": ["LS01", "LS02"],
#         "TrangThai": ["DangChay", "HoanThanh"],
#         "Site": ["Bac", "Trung"]
#     })

# def fake_giavon():
#     return pd.DataFrame({
#         "MaVT": ["CPU", "RAM"],
#         "Gia": [300, 100]
#     })

# def fake_alert():
#     return pd.DataFrame({
#         "MaKho": ["K01"],
#         "TenVT": ["CPU"],
#         "SoLuongTon": [5],
#         "MinStock": [10]
#     })

# # =========================
# # SIDEBAR
# # =========================
# with st.sidebar:
#     st.title("SCM System")

#     selected_site = st.selectbox("Chọn Site", ["All", "Bắc", "Trung", "Nam"])

#     st.divider()
#     st.info("Distributed Database Demo")

# # =========================
# # HEADER
# # =========================
# st.title("📊 SCM Distributed Dashboard")

# # =========================
# # TABS
# # =========================
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
#     "Overview",
#     "Inventory",
#     "Manufacturing",
#     "Costing",
#     "Transactions",
#     "Alerts"
# ])

# # =========================
# # TAB 1: OVERVIEW
# # =========================
# with tab1:
#     st.subheader("System Overview")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Total Inventory", "350")
#     col2.metric("Total Value", "$50,000")
#     col3.metric("Active LSX", "12")
#     col4.metric("Transactions", "120")

#     st.subheader("Inventory by Region")
#     df = fake_inventory()
#     st.bar_chart(df.set_index("TenKho"))

# # =========================
# # TAB 2: INVENTORY
# # =========================
# with tab2:
#     st.subheader("Inventory Lookup")

#     mavt = st.text_input("Nhập mã vật tư")

#     if st.button("Tra cứu"):
#         df = fake_inventory()
#         st.dataframe(df, use_container_width=True)

#         st.bar_chart(df.set_index("TenKho"))

# # =========================
# # TAB 3: MANUFACTURING
# # =========================
# with tab3:
#     st.subheader("Production Orders")

#     df = fake_lsx()

#     status = st.selectbox("Filter trạng thái", ["All", "DangChay", "HoanThanh"])

#     if status != "All":
#         df = df[df["TrangThai"] == status]

#     st.dataframe(df, use_container_width=True)

# # =========================
# # TAB 4: COSTING (HQ ONLY)
# # =========================
# with tab4:
#     st.subheader("Costing (HQ - Miền Nam)")

#     st.warning("Dữ liệu chỉ có tại Site Miền Nam")

#     df = fake_giavon()
#     st.dataframe(df, use_container_width=True)

# # =========================
# # TAB 5: TRANSACTIONS
# # =========================
# with tab5:
#     st.subheader("Transactions")

#     df = fake_transactions()

#     st.dataframe(df, use_container_width=True)

# # =========================
# # TAB 6: ALERTS
# # =========================
# with tab6:
#     st.subheader("Low Stock Alert")

#     df = fake_alert()

#     st.dataframe(df, use_container_width=True)

#     st.metric("Items below MinStock", len(df))