import streamlit as st

from services.finance_service import load_transactions

def show_income(conn):

    st.title("💰 Income Sources")

    df = load_transactions(conn)

    income_df = df[df["type"] == "Income"]

    st.dataframe(
        income_df,
        use_container_width=True
    )