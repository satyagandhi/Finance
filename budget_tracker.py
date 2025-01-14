import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for transactions
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

# Helper functions
def add_transaction(type_, amount, category):
    st.session_state["transactions"].append({"Type": type_, "Amount": amount, "Category": category})

def get_summary():
    df = pd.DataFrame(st.session_state["transactions"])
    income = df[df["Type"] == "Income"]["Amount"].sum() if not df.empty else 0
    expenses = df[df["Type"] == "Expense"]["Amount"].sum() if not df.empty else 0
    balance = income - expenses
    return income, expenses, balance

# App UI
st.title("Budget Tracker App")

# Input form
st.header("Add a Transaction")
with st.form("transaction_form"):
    col1, col2, col3 = st.columns(3)
    type_ = col1.selectbox("Type", ["Income", "Expense"])
    amount = col2.number_input("Amount", min_value=0.0, format="%.2f")
    category = col3.text_input("Category")
    submitted = st.form_submit_button("Add")
    if submitted and amount > 0 and category:
        add_transaction(type_, amount, category)
        st.success(f"{type_} of ${amount:.2f} in '{category}' added!")

# Display summary
st.header("Summary")
income, expenses, balance = get_summary()
st.metric("Total Income", f"${income:.2f}")
st.metric("Total Expenses", f"${expenses:.2f}")
st.metric("Balance", f"${balance:.2f}")

# Transaction history
st.header("Transaction History")
if st.session_state["transactions"]:
    df = pd.DataFrame(st.session_state["transactions"])
    st.dataframe(df)

    # Pie chart visualization
    st.subheader("Expense Breakdown")
    expense_data = df[df["Type"] == "Expense"]
    if not expense_data.empty:
        expense_summary = expense_data.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        expense_summary.plot.pie(ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_ylabel("")
        st.pyplot(fig)
else:
    st.info("No transactions added yet.")

