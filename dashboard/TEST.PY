import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

# =========================
# HELPER FUNCTION
# =========================
def fetch_api(endpoint):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code} at {endpoint}")
            return {"error": response.text}

    except Exception as e:
        print(f"🚨 Exception at {endpoint}: {e}")
        return {"error": str(e)}


# =========================
# CALL ALL APIs
# =========================
def collect_all_data():
    data = {
        "timestamp": datetime.now().isoformat(),

        "overview": fetch_api("/overview"),

        "inventory": {
            "summary": fetch_api("/inventory/summary"),
            "item_VT01": fetch_api("/inventory/VT01"),
            "by_warehouse": fetch_api("/inventory/by-warehouse"),
            "value_KHO_B01": fetch_api("/inventory/value/KHO_B01"),
        },

        "production": {
            "all_lsx": fetch_api("/lsx"),
            "running_lsx": fetch_api("/lsx?status=DangChay"),
        },

        "costing": {
            "giavon": fetch_api("/costing/giavon"),
        },

        "transactions": {
            "all": fetch_api("/transactions"),
            "nhap_month_4": fetch_api("/transactions/nhap?month=4"),
        },

        "alerts": {
            "low_stock": fetch_api("/alerts/low-stock"),
        },

        "global": {
            "inventory_VT01": fetch_api("/global/inventory/VT01"),
            "transaction_2024": fetch_api("/global/count-transactions?year=2024"),
        }
    }

    return data


# =========================
# EXPORT JSON
# =========================
def export_json(data, filename="scm_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Exported to {filename}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    all_data = collect_all_data()
    export_json(all_data)