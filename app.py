import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shop Daily Sales", layout="centered")
st.title("🛍️ Daily Sales Entry System")

# Initialize session state for storing sales data
if "sales_data" not in st.session_state:
    st.session_state["sales_data"] = pd.DataFrame(
        columns=["Product", "Quantity", "Price", "Discount (%)", "Total"]
    )

# ---------- Add Sale Form ----------
st.subheader("➕ Add New Sale")
with st.form("sales_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Product Name")
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
            new_row = pd.DataFrame([[product, quantity, price, discount, total]],
                                   columns=["Product", "Quantity", "Price", "Discount (%)", "Total"])
            st.session_state["sales_data"] = pd.concat(
                [st.session_state["sales_data"], new_row], ignore_index=True
            )
            st.success(f"✅ Sale for '{product}' added successfully!")

# ---------- Display Sales Table ----------
st.subheader("📊 Today's Sales Records")
if not st.session_state["sales_data"].empty:
    st.dataframe(st.session_state["sales_data"], use_container_width=True)

    total_qty = st.session_state["sales_data"]["Quantity"].sum()
    total_sales = st.session_state["sales_data"]["Total"].sum()

    st.markdown(f"**🧮 Total Quantity Sold:** {total_qty}")
    st.markdown(f"**💰 Total Sales Amount:** {total_sales:.2f}")
else:
    st.info("No sales data added yet.")

# ---------- Clear Records ----------
if st.button("🧹 Clear All Records"):
    st.session_state["sales_data"] = pd.DataFrame(
        columns=["Product", "Quantity", "Price", "Discount (%)", "Total"]
    )
    st.success("All records cleared ✅")
