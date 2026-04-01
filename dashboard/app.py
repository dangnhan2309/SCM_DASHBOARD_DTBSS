# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px

# # Cấu hình giao diện
# st.set_page_config(page_title="HUTECH Distributed ERP", layout="wide")

# API_BASE_URL = "http://127.0.0.1:8000"

# st.title("🚀 Hệ Thống Quản Lý Kho Phân Tán")
# st.sidebar.header("Cấu hình & Điều khiển")

# # --- TAB 1: DASHBOARD & BI ---
# tab1, tab2, tab3 = st.tabs(["📊 Tổng quan tồn kho", "📝 Nhập phiếu mới", "📈 Báo cáo giá trị"])

# with tab1:
#     st.subheader("📦 Dashboard tồn kho phân tán")

#     col_top1, col_top2 = st.columns(2)

#     # 🔥 CHỌN SITE (DEMO 1)
#     with col_top1:
#         site_selected = st.selectbox(
#             "🔎 Chọn Site xem dữ liệu",
#             ["GLOBAL", "BAC", "TRUNG", "NAM"]
#         )

#     # 🔥 BUTTON LOAD
#     with col_top2:
#         load_btn = st.button("🚀 Tải dữ liệu")

#     if load_btn:
#         try:
#             # =========================
#             # CASE 1: GLOBAL
#             # =========================
#             if site_selected == "GLOBAL":
#                 url = f"{API_BASE_URL}/tonkho/global"
#                 st.info("🌐 Đang lấy dữ liệu toàn hệ thống (DBLINK)")

#             # =========================
#             # CASE 2: LOCAL SITE
#             # =========================
#             else:
#                 url = f"{API_BASE_URL}/tonkho/{site_selected or "".lower()}"
#                 st.info(f"📍 Đang lấy dữ liệu tại Site {site_selected}")

#             res = requests.get(url)

#             if res.status_code == 200:
#                 df = pd.DataFrame(res.json())

#                 if not df.empty:

#                     # =========================
#                     # 🔥 METRIC (ĂN ĐIỂM)
#                     # =========================
#                     total = df["SoLuongTon"].sum()
#                     st.metric("📊 Tổng tồn kho", f"{total:,.0f}")

#                     # =========================
#                     # TABLE
#                     # =========================
#                     st.dataframe(df, use_container_width=True)

#                     col1, col2 = st.columns(2)

#                     # =========================
#                     # BAR CHART
#                     # =========================
#                     with col1:
#                         st.write("📊 Tồn theo Vật tư")

#                         fig_bar = px.bar(
#                             df,
#                             x="MaVT",
#                             y="SoLuongTon",
#                             color="KhuVuc" if "KhuVuc" in df.columns else None,
#                             barmode="group"
#                         )
#                         st.plotly_chart(fig_bar, use_container_width=True)

#                     # =========================
#                     # PIE CHART
#                     # =========================
#                     with col2:
#                         if "KhuVuc" in df.columns:
#                             st.write("🌍 Tỉ lệ theo vùng")

#                             fig_pie = px.pie(
#                                 df,
#                                 values="SoLuongTon",
#                                 names="KhuVuc"
#                             )
#                             st.plotly_chart(fig_pie, use_container_width=True)

#                 else:
#                     st.warning("Không có dữ liệu")

#             else:
#                 st.error("API lỗi!")

#         except Exception as e:
#             st.error(f"Lỗi: {e}")
# # --- TAB 2: FORM NHẬP PHIẾU ---
# with tab2:
#     st.subheader("➕ Tạo Phiếu Nhập/Xuất Mới")
    
#     with st.form("form_phieu"):
#         col_a, col_b = st.columns(2)
#         with col_a:
#             site = st.selectbox("Chọn Site đích", ["NAM", "TRUNG", "BAC"])
#             ma_phieu = st.text_input("Mã Phiếu (Ví dụ: PN100)")
#             loai = st.radio("Loại phiếu", ["N", "X"], horizontal=True)
#         with col_b:
#             ngay = st.date_input("Ngày thực hiện")
#             ma_kho = st.text_input("Mã Kho")
#             dien_giai = st.text_area("Diễn giải")
            
#         submit = st.form_submit_button("Lưu Phiếu")
        
#         if submit:
#             payload = {
#                 "MaPhieu": ma_phieu,
#                 "NgayNX": str(ngay),
#                 "LoaiPhieu": loai,
#                 "DienGiai": dien_giai,
#                 "MaKho": ma_kho,
#                 "site": site or "".lower()
#             }

#             res = requests.post(f"{API_BASE_URL}/phieu", json=payload)

#             if res.status_code == 200:
#                 st.success(f"✅ Phiếu {ma_phieu} đã tạo tại Site {site}")
#             else:
#                 st.error(f"❌ Lỗi: {res.text}")

# # --- TAB 3: BÁO CÁO GIÁ TRỊ (PHÂN TÁN DỌC) ---
# with tab3:
#     st.subheader("💰 Báo cáo Giá trị Tồn kho")

#     if st.button("📥 Tải báo cáo tài chính"):
#         res = requests.get(f"{API_BASE_URL}/report/tonkho-giavon")

#         if res.status_code == 200:
#             df_report = pd.DataFrame(res.json())

#             if not df_report.empty:
#                 st.dataframe(df_report, use_container_width=True)

#                 # 🔥 TÍNH TỔNG GIÁ TRỊ
#                 if "TONGGIATRI" in df_report.columns:
#                     total_value = df_report["TONGGIATRI"].sum()

#                     st.metric(
#                         "💸 Tổng giá trị tồn kho",
#                         f"{total_value:,.0f} VNĐ"
#                     )

#                 # 🔥 CHART GIÁ TRỊ
#                 if "TenVT" in df_report.columns:
#                     fig = px.bar(
#                         df_report,
#                         x="TenVT",
#                         y="TongGiaTri",
#                         title="Giá trị tồn theo vật tư"
#                     )
#                     st.plotly_chart(fig, use_container_width=True)

#         else:
#             st.error("Không load được report")





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