import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIG
# =========================
BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="SCM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body {
    background-color: #F8FAFC;
}

/* ===== CONTAINER ===== */
.block-container {
    padding-top: 2rem;
}

/* ===== METRIC CARD ===== */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.08);
    border: 1px solid #E2E8F0;
}

/* 🔥 FIX TEXT TRONG METRIC */
div[data-testid="stMetric"] label {
    color: #64748B !important;  /* text phụ */
    font-size: 14px;
    font-weight: 500;
}

div[data-testid="stMetric"] div {
    color: #1E293B !important;  /* số chính */
    font-size: 28px;
    font-weight: 700;
}

/* ===== HEADER ===== */
h1 {
    color: #1E293B;
}

h2, h3 {
    color: #334155;
}

/* ===== ALERT FIX ===== */
div[data-testid="stAlert"] {
    color: #1E293B !important;
}

/* ===== DATAFRAME HEADER ===== */
thead tr th {
    background-color: #EFF6FF !important;
    color: #1E3A8A !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #605B51;
}

/* ===== BUTTON ===== */
button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 10px !important;
}

button:hover {
    background-color: #1D4ED8 !important;
}

</style>
""", unsafe_allow_html=True)
tab1, tab2= st.tabs([
    "Overview",
    "🧪 SQL Test"
])

with tab1:
    # =========================
    # API CALL
    # =========================
    @st.cache_data(ttl=60)
    def call_api(endpoint):
        try:
            res = requests.get(f"{BASE_URL}{endpoint}")
            if res.status_code == 200:
                return res.json()
            return {}
        except:
            return {}

    # =========================
    # DATA FUNCTIONS
    # =========================
    def get_overview():
        return call_api("/overview") or {}

    def get_inventory_summary():
        return pd.DataFrame(call_api("/inventory/summary") or [])

    def get_inventory_item(mavt):
        return pd.DataFrame(call_api(f"/inventory/{mavt}") or [])

    def get_inventory_by_warehouse():
        return pd.DataFrame(call_api("/inventory/by-warehouse") or [])

    def get_inventory_value():
        data = call_api("/inventory/value/KHO_B01")
        return pd.DataFrame(data.get("data", []))

    def get_lsx(status=None):
        if status and status != "All":
            return pd.DataFrame(call_api(f"/lsx?status={status}") or [])
        return pd.DataFrame(call_api("/lsx") or [])

    def get_giavon():
        return pd.DataFrame(call_api("/costing/giavon") or [])

    def get_transactions(month=None):
        if month:
            return pd.DataFrame(call_api(f"/transactions/nhap?month={month}") or [])
        return pd.DataFrame(call_api("/transactions") or [])

    def get_alerts():
        return pd.DataFrame(call_api("/alerts/low-stock") or [])

    def get_global_inventory():
        data = call_api("/global/inventory/VT01")
        return data[0]["total"] if data else 0

    # =========================
    # SIDEBAR
    # =========================
    with st.sidebar:
        st.title("🚀 SCM System")
        st.caption("Distributed Database")
        st.divider()

        mavt = st.text_input("🔍 Mã vật tư", "VT01")
        month = st.slider("📅 Tháng", 1, 12, 4)

    # =========================
    # HEADER
    # =========================
  

    overview = get_overview()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Inventory", overview.get("total_inventory", 0))
    col2.metric("LSX", overview.get("total_lsx", 0))
    col3.metric("Transactions", overview.get("total_transactions", 0))
    col4.metric("Global VT01", get_global_inventory())

    # =========================
    # INVENTORY
    # =========================
    st.subheader("📦 Inventory")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Theo Site")
        df = get_inventory_summary()

        if not df.empty:
            df = df.rename(columns={
                "site": "Site",
                "total_quantity": "Quantity"
            })
            st.bar_chart(df.set_index("Site"))

    with col2:
        st.markdown("### Theo Kho")
        df_wh = get_inventory_by_warehouse()

        if not df_wh.empty:
            df_wh = df_wh.groupby("MAKHO")["SOLUONGTON"].sum().reset_index()
            st.bar_chart(df_wh.set_index("MAKHO"))

    # =========================
    # ITEM LOOKUP
    # =========================
    st.subheader("🔍 Tra cứu vật tư")

    df_item = get_inventory_item(mavt)

    if not df_item.empty:
        df_item = df_item.groupby("MAKHO")["SOLUONGTON"].sum().reset_index()
        st.dataframe(df_item, use_container_width=True)

    # =========================
    # VALUE
    # =========================
    st.subheader("💰 Inventory Value (KHO_B01)")

    df_val = get_inventory_value()

    if not df_val.empty:
        st.dataframe(df_val, use_container_width=True)

        total_value = df_val["THANHTIEN"].sum()
        st.metric("Total Value", f"{total_value:,}")

    # =========================
    # MANUFACTURING
    # =========================
    st.subheader("🏭 Production")

    status = st.selectbox("Trạng thái", ["All", "DangChay", "HoanThanh"])

    df_lsx = get_lsx(status)

    if not df_lsx.empty:
        st.dataframe(df_lsx, use_container_width=True)

    # =========================
    # COSTING
    # =========================
    st.subheader("📊 Costing")

    df_cost = get_giavon()

    if not df_cost.empty:
        st.dataframe(df_cost, use_container_width=True)

    # =========================
    # TRANSACTIONS
    # =========================
    st.subheader("📑 Transactions")

    df_trans = get_transactions(month)

    if not df_trans.empty:
        st.dataframe(df_trans, use_container_width=True)

    # =========================
    # ALERTS
    # =========================
    st.subheader("🚨 Low Stock")

    df_alert = get_alerts()

    if not df_alert.empty:
        st.dataframe(df_alert, use_container_width=True)
        st.metric("⚠️ Items thiếu", len(df_alert))

# =========================
# TAB 7: SQL TEST
# =========================
with tab2:
    st.subheader("🧪 Distributed SQL Testing")

    st.info("Test các câu truy vấn & Stored Procedure trong hệ phân tán")

    # =========================
    # 1. VIEW - LOW STOCK BAC
    # =========================
    with st.expander("1️⃣ View Cảnh Báo Hết Hàng (Miền Bắc)"):
        st.write("""
        Hiển thị vật tư có tồn kho < MinStock tại miền Bắc
        """)

        if st.button("Chạy View", key="view1"):
            df = get_alerts()
            if not df.empty:
                st.dataframe(df, use_container_width=True)

    # =========================
    # 2. QUERY NHẬP TRUNG
    # =========================
    with st.expander("2️⃣ Phiếu nhập tháng này - Miền Trung"):
        st.write("Loại phiếu = NhapMua")

        if st.button("Chạy Query", key="query2"):
            df = get_transactions(month)
            if not df.empty:
                df = df[df["loaiphieu"].str.contains("Nhap", case=False)]
                st.dataframe(df, use_container_width=True)

    # =========================
    # 3. STORED PROC - SEARCH VT
    # =========================
    with st.expander("3️⃣ SP: Tìm vật tư toàn quốc"):
        st.write("Tìm tồn kho vật tư trên toàn hệ thống")

        mavt_sp = st.text_input("Nhập MaVT", "VT01", key="sp1")

        if st.button("Chạy SP", key="btn_sp1"):
            df = get_inventory_item(mavt_sp)

            if not df.empty:
                df = df.groupby("MAKHO")["SOLUONGTON"].sum().reset_index()
                df = df.sort_values(by="SOLUONGTON", ascending=False)

                st.dataframe(df, use_container_width=True)

    # =========================
    # 4. STORED PROC VALUE
    # =========================
    with st.expander("4️⃣ SP: Tính giá trị tồn kho"):
        st.write("JOIN tồn kho + giá vốn (Nam)")

        if st.button("Tính giá trị", key="sp2"):
            df = get_inventory_value()

            if not df.empty:
                st.dataframe(df)

                total = df["THANHTIEN"].sum()
                st.success(f"Tổng giá trị: {total:,}")

    # =========================
    # 5. GLOBAL INVENTORY
    # =========================
    with st.expander("5️⃣ Global Inventory (DATALINK)"):
        st.write("Tổng tồn kho toàn quốc cho 1 vật tư")

        if st.button("Chạy Global Query", key="q5"):
            total = get_global_inventory()
            st.metric("Tổng tồn VT01", total)

    # =========================
    # 6. TRIGGER DEMO
    # =========================
    with st.expander("6️⃣ Trigger Bảo vệ định mức"):
        st.write("""
        Nếu có LSX đang chạy → không cho update định mức
        """)

        if st.button("Kiểm tra Trigger", key="trg"):
            df = get_lsx("DangChay")

            if not df.empty:
                st.error("❌ Có lệnh sản xuất đang chạy → KHÔNG ĐƯỢC UPDATE")
            else:
                st.success("✅ Không có LSX → Cho phép update")

    # =========================
    # 7. COUNT TRANSACTIONS
    # =========================
    with st.expander("7️⃣ COUNT Phiếu toàn hệ thống "):
        st.write("Đếm số phiếu bằng distributed COUNT")
        year = st.text_input("Nhập năm ", "2024", key="count_year")

        if st.button("Chạy COUNT", key="count"):
            data = call_api(f"/global/count-transactions?year={year}")

            if data:
                st.metric("Tổng phiếu", data[0]["total"])