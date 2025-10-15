import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("🛒 Daily Sales Dashboard")

# Initialize session state
if "sales_data" not in st.session_state:
    st.session_state["sales_data"] = pd.DataFrame(
        columns=["Timestamp", "Product", "Category", "Quantity", "Price", "Discount (%)", "Total"]
    )

# ---------- Add Sale Form ----------
st.subheader("➕ Add New Sale")
with st.form("sales_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Product Name")
        category = st.text_input("Category (optional)")
        quantity = st.number_input("Quantity", min_value=1, step=1)
    with col2:
        price = st.number_input("Price per Unit", min_value=0.0, step=0.1)
        discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=0.1)

    submitted = st.form_submit_button("Add Sale")
    if submitted:
        if not product.strip():
            st.warning("⚠️ Please enter a product name.")
        else:
            total = quantity * price * (1 - discount / 100)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([[timestamp, product, category, quantity, price, discount, total]],
                                   columns=["Timestamp", "Product", "Category", "Quantity", "Price", "Discount (%)", "Total"])
            st.session_state["sales_data"] = pd.concat(
                [st.session_state["sales_data"], new_row], ignore_index=True
            )
            st.success(f"✅ Sale for '{product}' added successfully!")

# ---------- Display Table ----------
st.subheader("📊 Today's Sales Records")
data = st.session_state["sales_data"]

if not data.empty:
    # Filter by product
    product_filter = st.text_input("🔍 Filter by product name")
    if product_filter:
        data_display = data[data["Product"].str.contains(product_filter, case=False, na=False)]
    else:
        data_display = data.copy()

    st.dataframe(data_display.sort_values(by="Timestamp", ascending=False), use_container_width=True)

    # ---------- Summary Table ----------
    st.subheader("🧮 Summary by Product")
    summary = data.groupby("Product")[["Quantity", "Total"]].sum().reset_index()
    st.dataframe(summary, use_container_width=True)

    # ---------- Charts ----------
    st.subheader("📈 Sales Charts")

    col1, col2 = st.columns(2)

    # Bar chart: Total sales per product
    with col1:
        st.markdown("**💰 Total Sales per Product**")
        bar_chart = summary.set_index("Product")["Total"]
        st.bar_chart(bar_chart)

    # Pie chart: Sales distribution by category
    with col2:
        st.markdown("**📂 Sales Distribution by Category**")
        category_summary = data.groupby("Category")["Total"].sum()
        st.pyplot(category_summary.plot.pie(autopct="%1.1f%%", figsize=(5, 5)).figure)

    # Line chart: Sales trend during the day
    st.markdown("**⏱️ Sales Trend Over Time**")
    data["Timestamp_dt"] = pd.to_datetime(data["Timestamp"])
    trend = data.groupby("Timestamp_dt")["Total"].sum().reset_index()
    st.line_chart(trend.set_index("Timestamp_dt")["Total"])

else:
    st.info("No sales data added yet.")

# ---------- Clear Records ----------
if st.button("🧹 Clear All Records"):
    st.session_state["sales_data"] = pd.DataFrame(
        columns=["Timestamp", "Product", "Category", "Quantity", "Price", "Discount (%)", "Total"]
    )
    st.success("All records cleared ✅")
