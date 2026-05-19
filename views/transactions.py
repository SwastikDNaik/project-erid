import streamlit as st

from services.finance_service import load_transactions

def show_transactions(conn):

    st.title("💳 Transactions")

    df = load_transactions(conn)

    st.dataframe(
        df,
        use_container_width=True
    )