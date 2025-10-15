import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# -----------------------------
# 📌 File Setup
# -----------------------------
TODAY = datetime.now().strftime("%Y-%m-%d")
DATA_DIR = "sales_records"
os.makedirs(DATA_DIR, exist_ok=True)
DAILY_FILE = os.path.join(DATA_DIR, f"sales_{TODAY}.xlsx")

# -----------------------------
# 🧠 Load Existing Data
# -----------------------------
def load_daily_sales():
    if os.path.exists(DAILY_FILE):
        return pd.read_excel(DAILY_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Product", "Quantity", "Price", "Discount (%)", "Total"])

# -----------------------------
# 💾 Save Data to Excel
# -----------------------------
def save_to_excel(df):
    with pd.ExcelWriter(DAILY_FILE, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Daily Sales')
        worksheet = writer.sheets['Daily Sales']
        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)

# -----------------------------
# 🌐 Streamlit App Config
# -----------------------------
st.set_page_config(page_title="🧾 Daily Sales Entry", layout="centered")
st.title("🧾 Daily Sales Entry & Excel Export")

# Initialize session state
if "sales_data" not in st.session_state:
    st.session_state.sales_data = load_daily_sales()

# -----------------------------
# 📝 Sales Entry Form
# -----------------------------
st.subheader(f"📅 Enter Sales for {TODAY}")

with st.form("sales_form"):
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Product Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
    with col2:
        price = st.number_input("Price (per unit)", min_value=0.0, step=0.01, format="%.2f")
        discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=0.1)

    submitted = st.form_submit_button("➕ Add Entry")
    if submitted:
        if product.strip() == "":
            st.error("⚠️ Please enter product name.")
        else:
            total_before_discount = quantity * price
            total_after_discount = total_before_discount * (1 - discount / 100)

            entry = {
                "Date": TODAY,
                "Product": product,
                "Quantity": quantity,
                "Price": price,
                "Discount (%)": discount,
                "Total": round(total_after_discount, 2)
            }

            # Append to session and file
            st.session_state.sales_data = pd.concat(
                [st.session_state.sales_data, pd.DataFrame([entry])],
                ignore_index=True
            )
            save_to_excel(st.session_state.sales_data)
            st.success(f"✅ Entry saved for **{product}**")

# -----------------------------
# 📊 Sales Records Table
# -----------------------------
st.subheader("📊 Daily Sales Records")

if len(st.session_state.sales_data) == 0:
    st.info("No sales records yet. Add entries above.")
else:
    st.dataframe(st.session_state.sales_data, use_container_width=True)

    total_qty = st.session_state.sales_data["Quantity"].sum()
    total_sales = st.session_state.sales_data["Total"].sum()

    st.markdown(f"**🧮 Total Quantity Sold:** {total_qty}")
    st.markdown(f"**💰 Total Sales Amount:** ₹ {round(total_sales, 2)}")

    # -----------------------------
    # ⬇️ Download Excel File
    # -----------------------------
    with open(DAILY_FILE, "rb") as file:
        st.download_button(
            label="⬇️ Download Daily Excel File",
            data=file,
            file_name=f"sales_{TODAY}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -----------------------------
# 🗂️ View Saved Files
# -----------------------------
st.markdown("---")
st.subheader("📂 Previous Daily Files")
files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")])
if files:
    for f in files:
        file_path = os.path.join(DATA_DIR, f)
        with open(file_path, "rb") as file:
            st.download_button(
                label=f"⬇️ Download {f}",
                data=file,
                file_name=f,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f
            )
else:
    st.info("No saved files yet.")
